# Slurm

## Node

In Slurm, a **partition** is a named group of computer nodes that users can submit jobs to. Each **node** is one computer machine (or server) in the cluster, and it can have multiple GPUs. Use the following command to retrieve information about nodes in the cluster:

```bash
sinfo -p beacon -N -o "%.12N %.8t %.8c %.10m %.12e %.35G %.30f"
```

Option `-p beacon` specifies the `beacon` partition, flag `-N` means show information node-by-node, and option `-o` specifies the output format.

- `%N`: Node name
- `%t`: Node state, such as `idle`, `alloc`, `mix`, and `down`
- `%c`: Number of CPUs/cores
- `%m`: Memory size, usually MB
- `%e`: Free memory, usually MB
- `%G`: GRES, often GPU type/count

Here, four common node states are

- `idle`: Node is free and not currently allocated to jobs
- `alloc`: Node is fully allocated to one or more jobs
- `mix`: Node is partially allocated; some resources are in use, some may still be free
- `down`: Node is unavailable due to failure, maintenance, or admin action

An example output of the command is:

```text
NODELIST     STATE    CPUS     MEMORY     FREE_MEM     GRES
ihccs200     alloc    128      2060000    900000       gpu:nvidia_h200:8(S:0-1)
ihccs201     mix      128      2060000    1200000      gpu:nvidia_h200:8(S:0-1)
ihccs202     idle     128      2060000    2060000      gpu:nvidia_h200:4(S:0-1)
```

## Partition

In Slurm, a **job** is a request you submit to the cluster asking Slurm to run some work for you. A **queue** is the waiting line of jobs that Slurm has not run yet. Use the following command to check the queue of partition `beacon`:

```bash
squeue -p beacon
```

An example output is:

```text
JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
56926    beacon      rf3     yige PD       0:00      1 (AssocMaxJobsLimit)
56932    beacon       FL suzhang1 PD       0:00      1 (Resources)
56933    beacon       FL suzhang1 PD       0:00      1 (Priority)
60185    beacon     tqgm      cys PD       0:00      1 (Priority)
25868    beacon     srun   shengz PD       0:00      1 (JobHeldUser)
54556    beacon       FL suzhang1  R 2-01:09:05      1 ihccs212
56920    beacon      aa7     yige  R 1-08:35:36      1 ihccs212
```

The meaning of each column:

- `JOBID`: A unique identifier of a job.
- `PARTITION`: Partition name, which has been specified in the command.
- `NAME`: Job name.
- `ST`: Job state.
- `TIME`: How long it has been running. In `1-08:35:36`, `1-` means 1 day.
- `NODES`: Number of nodes requested or used.
- `NODELIST(REASON)`: where it is running, or why it is pending.

Common job states include:

- `R` - running
- `PD` - pending / waiting
- `CG` - completing
- `CD` - completed
- `F` - failed
- `CA` - cancelled

Common reasons why a job is pending include:

- `(Resources)`: There are not enough free matching resources right now.
- `(Priority)`: The job is eligible to run, but other jobs have higher scheduling priority.
- `(ReqNodeNotAvail)`:
- `(AssocMaxJobsLimit)`: The user has submitted too many jobs.
- `(JobHeldUser)`: The user has put a hold on it.
- `(JobHeldAdmin)`: An administrator has put an admin hold on it.

If two jobs A and B request the same resources, and they are marked with `(Resources)` and `(Priority)`, respectively, then in most cases, job A will be processed ahead of job B.

## Estimated Start Time

Suppose we have a job whose ID is `101`, and we want to know when it can start. We can get the estimated start time with the following command:

```bash
squeue --start -j 101
```

Here, flag `--start` adds a `START_TIME` column, and option `-j` specifies the ID of the job.

An example output is

```text
JOBID PARTITION     NAME     USER ST          START_TIME  NODES SCHEDNODES           NODELIST(REASON)
101      beacon gpu_train   alice PD 2026-05-26T14:30:00      1 beacon-node03        (Resources)
```

The estimated start time is `2026-05-26T14:30:00`. Note that the time is an estimate, not a promise. You can also see something like this:

```text
JOBID PARTITION     NAME     USER ST START_TIME NODES SCHEDNODES NODELIST(REASON)
101      beacon gpu_train   alice PD        N/A     1 (null)      (Priority)
```

In this case, Slurm currently does not have a reliable estimated start time for the job.
