Task
---

You are going to simulate client stress on the ScyllaDB database and analyze the stress results.

The exercise consists of two parts: 

 1. Deploying single node scylla cluster on docker and getting to know the cassandra-stress command.

 2. Coding a small program that will run several stress threads of cassandra-stress and analyze their results.



### Deploying single node scylla cluster on docker

 • Follow the steps here to deploy a single node scylla cluster (you can stop after "Run nodetool utility" step).
 
 • Exercise the running the cassandra-stress command by using the command:
`docker exec some-scylla cassandra-stress write duration=10s -rate threads=10 -node node_ip_from_nodetool_output`

 • Understanding the cassandra-stress results output.
When cassandra-stress output completes it provides a results summary that looks like this:
```
Results:

﻿Op rate : 2,387 op/s [WRITE: 2,387 op/s]
Partition rate : 2,387 pk/s [WRITE: 2,387 pk/s]
Row rate : 2,387 row/s [WRITE: 2,387 row/s]
Latency mean : 4.0 ms [WRITE: 4.0 ms]
Latency median : 2.8 ms [WRITE: 2.8 ms]
Latency 95th percentile : 10.5 ms [WRITE: 10.5 ms]
Latency 99th percentile : 19.9 ms [WRITE: 19.9 ms]
Latency 99.9th percentile : 69.5 ms [WRITE: 69.5 ms]
Latency max : 115.7 ms [WRITE: 115.7 ms]
Total partitions : 7,292 [WRITE: 7,292]
Total errors : 0 [WRITE: 0]
Total GC count : 0
Total GC memory : 0.000 KiB
Total GC time : 0.0 seconds
Avg GC time : NaN ms
StdDev GC time : 0.0 ms
Total operation time : 00:00:03

END
```

### Analysis and runner program

The Analysis program will run concurrently N stress commands while each one of them will run in a separate thread.
The analysis program should parse the results summary of each of the stress threads and print the aggregated summary of all threads.



Requirements:

 • Number of concurrent stress commands to run will be received as a command line argument.

 • Each stress command runtime duration may be different.

 • The program should print an aggregated summary with the details below.

 • Number of stress processes that ran.

 • Calculated aggregation of "Op rate" (sum).

 • Calculated average of "Latency mean" (average).

 • Calculated average of "Latency 99th percentile" (average).

 • Standard deviation calculation of all "Latency max" results.
