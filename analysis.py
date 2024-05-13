#!/usr/bin/env python3

import subprocess
import re
import locale
import statistics
import asyncio
import argparse
from container_utils import ensure_docker


locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
RESULTS = {
        'Op rate': {
            'aggregate_fun': sum,
            'output_format': "{: <25} [sum]     : {} op/s"
        },
        'Latency mean': {
            'aggregate_fun': statistics.mean,
            'output_format': "{: <25} [average] : {} ms"
        },
        'Latency 99th percentile': {
            'aggregate_fun': statistics.mean,
            'output_format': "{: <25} [average] : {} ms"
        },
        'Latency max': {
            'aggregate_fun': statistics.mean,
            'output_format': "{: <25} [std dev] : {} ms"
        },
    }


def get_node_ip(name):
    cmd = f"docker exec -it {name} nodetool status"
    process = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, encoding='utf-8')
    output, _ = process.communicate()
    matches = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', output)
    if len(matches) != 1:
        raise Exception(f"Could not find node ip address:\nOutput:\n{output}")
    return matches[0]


async def run_cassandra_stress(name, node_ip):
    cmd = f'docker exec {name} cassandra-stress write duration=10s -rate threads=10 -node {node_ip}'
    process = await asyncio.create_subprocess_shell(cmd, shell=True, stderr=asyncio.subprocess.STDOUT, stdout=asyncio.subprocess.PIPE)
    output, _ = await process.communicate()
    lines = output.decode().splitlines()
    results = lines[lines.index("Results:")+1:-2]
    return interpret_results(results)


def interpret_results(lines):
    results = dict((k, None) for k in RESULTS)

    for line in lines:
        name, raw_value = line.split(':', 1)
        name = name.strip()
        raw_value = raw_value.strip()
        if name in results:
            # some numbers have commas as a thousands delimitator, so int() or float() would not work
            results[name] = locale.atof(raw_value.split(' ')[0])    

    if not all(results.values()):
        not_found = ', '.join(k for k in results if not results[k])
        raise Exception(f'Could not find results for: {not_found}')
    
    return results


def results_aggregator(list_of_results):
    print('Number of concurrent stress tests   :', len(list_of_results))
    for k in RESULTS:
        aggregate = RESULTS[k]['aggregate_fun'](r[k] for r in list_of_results)
        print(RESULTS[k]['output_format'].format(k, aggregate))


async def main():
    parser = argparse.ArgumentParser(
        description="Run cassandra stress tests on a scylladb docker container"
    )
    parser.add_argument(
        '-n', 
        dest='number_of_tests',
        type=int,
        default=2,  # minimun nr of results required to be able to calculate stdev
        help='The number of concurent stress tests to run'
        )
    parser.add_argument(
        '--name', 
        dest='name',
        type=str,
        default='scylla-stress',
        help='The name of the docker container to run stress tests on'
        )
    args = parser.parse_args()
    ensure_docker(args.name)
    node_ip = get_node_ip(args.name)
    tests = [run_cassandra_stress(args.name, node_ip) for _ in range(args.number_of_tests)]
    results = await asyncio.gather(*tests)
    results_aggregator(results)

if __name__ == "__main__":
    asyncio.run(main())
