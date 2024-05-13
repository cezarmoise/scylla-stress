#!/usr/bin/env python3

from subprocess import Popen, STDOUT, PIPE
import re
import locale
import statistics


locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
CONTAINER_NAME = "scylla-stress"


def get_node_ip(name):
    cmd = f"docker exec -it {name} nodetool status"
    process = Popen(cmd, shell=True, stderr=STDOUT, stdout=PIPE, encoding='utf-8')
    output, _ = process.communicate()
    matches = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', output)
    if len(matches) != 1:
        raise Exception(f"Could not find node ip address:\nOutput:\n{output}")
    return matches[0]


def run_cassandra_stress(name, node_ip):
    cmd = f'docker exec {name} cassandra-stress write duration=10s -rate threads=10 -node {node_ip}'
    process = Popen(cmd, shell=True, stderr=STDOUT, stdout=PIPE, encoding='utf-8')
    output, _ = process.communicate()
    lines = output.splitlines()
    results = lines[lines.index("Results:")+1:-2]
    return interpret_results(results)


def interpret_results(lines):
    results = {
        'Op rate': None,
        'Latency mean': None,
        'Latency 99th percentile': None,
        'Latency max': None
    }

    for line in lines:
        name, raw_value = line.split(':', 1)
        name = name.strip()
        raw_value = raw_value.strip()
        if name in results:
            results[name] = locale.atof(raw_value.split(' ')[0])    

    if not all(results.values()):
        not_found = ', '.join(k for k in results if not results[k])
        raise Exception(f'Could not find results for: {not_found}')
    
    return results


def results_agregator(list_of_results):
    units = {
        'Op rate': 'op/s',
        'Latency mean': 'ms',
        'Latency 99th percentile': 'ms',
        'Latency max': 'ms'
    }

    op = {
        'Op rate': sum,
        'Latency mean': statistics.mean,
        'Latency 99th percentile': statistics.mean,
        'Latency max': statistics.stdev
    }

    for k, v in units.items():
        aggragate = op[k](r[k] for r in list_of_results)
        print(f'{k}: {aggragate:.2f} {v}')


if __name__ == "__main__":
    node_ip = get_node_ip(CONTAINER_NAME)
    results = run_cassandra_stress(CONTAINER_NAME, node_ip)
    results2 = run_cassandra_stress(CONTAINER_NAME, node_ip)
    results_agregator([results, results2])