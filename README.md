# Scylla DB Stress Test results agregator


Example usage

```
$ python3 analysis.py -n 5

Number of concurrent stress tests   : 5
Op rate                   [sum]     : 54952.0 op/s
Latency mean              [average] : 0.3 ms
Latency 99th percentile   [average] : 0.8 ms
Latency max               [std dev] : 17.5 ms
```

> Note:  
> The analysis program will start/create a docker container using the default ports each time  
> If there are multiple containers using those ports, the program will fail


### Tasks:

- [x] Get node ip address using the nodetool command
- [x] Run the the cassandra-stress command
- [x] Extract the needed results fron the output of the stress command
- [x] Run the stress command multiple times and aggregate the results
- [x] Parallelize running the stress command
- [x] Add command-line arguments for number of concurrent stress commands
- [x] Consolidate code regarding which stats from the output are selected
- [x] Improve result formating
- [x] Ensure docker container exists and it is started