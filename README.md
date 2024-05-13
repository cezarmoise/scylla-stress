# Scylla DB Stress Test results agregator


Create and start a scylladb docker container  
```
$ docker run --name scylla-stress --hostname scylla-stress -d scylladb/scylla
```

If already created, just start it  
```
$ docker start scylla-stress
```


Run `analysis.py` 
```
$ python3 analysis.py -n 10
Number of concurrent stress tests   : 10
Op rate                   [sum]     : 59392.0 op/s
Latency mean              [average] : 1.6 ms
Latency 99th percentile   [average] : 11.35 ms
Latency max               [std dev] : 39.06 ms
```


Ensure there is no other container started on the same ports.
In the example bellow, the program will fail to connect to scylla
```
$ docker ps
CONTAINER ID   IMAGE             COMMAND                  CREATED         STATUS         PORTS                                                            NAMES
a0dc02645480   scylladb/scylla   "/docker-entrypoint.…"   7 seconds ago   Up 7 seconds   22/tcp, 7000-7001/tcp, 9042/tcp, 9160/tcp, 9180/tcp, 10000/tcp   scylla-stress2
0cf66f788801   scylladb/scylla   "/docker-entrypoint.…"   24 hours ago    Up 2 minutes   22/tcp, 7000-7001/tcp, 9042/tcp, 9160/tcp, 9180/tcp, 10000/tcp   scylla-stress
```


### Tasks:

- [x] Get node ip address using the nodetool command
- [x] Run the the cassandra-stress command
- [x] Extract the needed results fron the output of the stress command
- [x] Run the stress command multiple times and aggregate the results
- [x] Parallelize running the stress command
- [x] Add command-line arguments for number of concurrent stress commands
- [x] Consolidate code regarding which stats from the output are selected
- [x] Improve result formating
