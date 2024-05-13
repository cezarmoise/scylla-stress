#!/usr/bin/env python3
import subprocess
from time import sleep

def ensure_docker(name):
    if container_is_running(name):
        print(f'Container {name} is running')
        return
    
    if container_exists(name):
        print(f'Container {name} is starting')
        cmd = f"docker start {name}"
        process = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, encoding='utf-8')
        output, _ = process.communicate()
        if process.returncode != 0:
            raise Exception(f'Error while starting container {name}:\n{output}')
        sleep(30)  # after starting the container, the connection to scylla is not available imediately
    else:
        print(f'Container {name} is being created')
        cmd = f'docker run --name {name} --hostname {name} -d scylladb/scylla'
        process = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, encoding='utf-8')
        output, _ = process.communicate()
        if process.returncode != 0:
            raise Exception(f'Error while creating container {name}:\n{output}')
        sleep(30)  # after starting the container, the connection to scylla is not available imediately


def container_exists(name):
    cmd = f"docker ps -a"
    process = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, encoding='utf-8')
    output, _ = process.communicate()
    lines = output.splitlines()
    for line in lines[1:]:
        if line.split(' ')[-1] == name:
            return True

    return False


def container_is_running(name):
    cmd = f"docker ps"
    process = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, encoding='utf-8')
    output, _ = process.communicate()
    lines = output.splitlines()
    for line in lines[1:]:
        if line.split(' ')[-1] == name:
            return True

    return False
