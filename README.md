# Scylla DB Stress Test results agregator


### Steps:

1. Create and start a scylladb docker container  
    `docker run --name scylla-stress --hostname scylla-stress -d scylladb/scylla`  
    If already created, just start it  
    `docker start scylla-stress`

2. Run `python3 analysis.py`


### Tasks:

- [x] Get node ip address using the nodetool command
- [x] Run the the cassandra-stress command
- [x] Extract the needed results fron the output of the stress command
- [x] Run the stress command multiple times and aggregate the results
- [x] Parallelize running the stress command
- [ ] Add command-line arguments for number of concurrent stress commands
