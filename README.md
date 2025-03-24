
# flower-samples

**Experimental Repository**  
Samples demonstrating how to scale Flower.ai simulations on a Ray Cluster.

---

## Overview

This repository provides experimental examples showcasing Flower.ai simulations running distributed across multiple nodes and GPUs on a Ray Cluster.

### Current Sample

- [`quickstart-pytorch`](quickstart-pytorch): Based on the [Flower quickstart PyTorch example](https://github.com/adap/flower/tree/96f996207da7e3147506e4be4fe374cb39243e28/examples/quickstart-pytorch)

---

## Recommended Versions

⚠️ **Important:**  
The Ray version used on the application needs to match the Ray Cluster.

- **When setting up a Ray Cluster**: Mind that Flower `0.16.0` simulation [requires Ray `2.31.0`](https://github.com/adap/flower/blob/8ba9db597b0309a7d34c7595d89a92f378733428/pyproject.toml#L80).
- **For IOG Ray clusters**: Base image for [IOG Ray Cluster](https://cloud.io.net/) is Ray `2.30.0`. Use the customized Flower fork at [IOG-Foundation/flower@iog-ray-cluster-2.30.0](https://github.com/IOG-Foundation/flower/tree/iog-ray-cluster-2.30.0).
  - besides custom pinned ray version, it includes [minor changes](https://github.com/IOG-Foundation/flower/commits/iog-ray-cluster-2.30.0/) which could be merged to the main repo if it makes sense for the official release, such as [allow ray nodes nodes to have zero resources](https://github.com/IOG-Foundation/flower/commit/10c9bbf7625e0426e0f76bb3a2497c3068b03c3a) and [flag to supress deprecation warning](https://github.com/IOG-Foundation/flower/commit/aeb8279f301d1780cc52739fe90b878817f2f588).

## How to Execute

Samples replicate the original Flower examples with minor adjustments and configured environment dependencies for convenience.

For the example [`quickstart-pytorch`](quickstart-pytorch):

```bash
git clone https://github.com/IOG-Foundation/flower-samples.git
cd flower-samples/quickstart-pytorch
```

### Standard Execution (for Reference)

Assuming you are familiar with the common execution of a Flower simulation and setup as described on the base [readme](quickstart-pytorch/README.md).

For reference, that's a standard execution:

```bash
flwr run . --run-config "num-server-rounds=5"
```

### Ray Job Submission

When submitting the script as a Ray Job, there is no need for local dependencies to be installed (except a matching Ray version `2.31.0`). If you want to submit to your local Ray Cluster, include the ray dashboard on your local environment (`pip install ray[default]==2.31.0`).  

```bash
ray job submit \
--runtime-env-json '{"working_dir": ".", "pip": "requirements.txt"}' \
-- flwr run . --run-config "num-server-rounds=5"
```

**Notes:**

- The `working_dir` is propagated to all Ray nodes.
- The runtime environment is configured on the worker nodes at submission. Subsequent submissions may leverage the cached environment.
- Specify the cluster address with `--address` if needed ([Ray Jobs CLI Reference](https://docs.ray.io/en/latest/cluster/running-applications/job-submission/cli.html)).
- The job command to be executed is defined after `--`.

---

#### Intermediate Script `flwr_run.py`

When using the intermediate script `flwr_run.py` to call the Flower CLI, have it available on `working_dir`. Then:

```bash
ray job submit \
--runtime-env-json '{"working_dir": ".", "pip": "requirements.txt"}' \
-- python flwr_run.py . --run-config "num-server-rounds=5"
```

As noted, `python flwr_run.py .`  is equivalent to `flwr run . `. All Flower simulation arguments are directly forwarded.

🔧 **Purpose of `flwr_run.py`:**  
Use this script to execute custom code or configurations prior to invoking `flwr run`. Modify it if your simulation needs specific environment setups, dynamic parameters, or pre-processing tasks not directly supported by Flower CLI. Possible applications: trigger in advance cluster autoscaling based on the request, as flower simulation will define the distribution based on the resources which are already available; evaluate the request to tune/adapt the resources when passing to the Flower CLI, as some configurations combination (of clients resources and number of supernodes) might allocate resources which will be blocked on wait, setting a sequential undesired pipeline, specially if resources available are much superior than the number of num-supernodes configured.

---

#### For Conda env

To use conda as the base environment:

```bash
ray job submit \
--runtime-env-json '{"working_dir": ".", "conda": "conda-env.yml"}' \
-- flwr run . --run-config "num-server-rounds=5"
```

---

### IOG Ray Cluster Job Submission

Dependencies below use customized Flower fork at [IOG-Foundation/flower/iog-ray-cluster-2.30.0](https://github.com/IOG-Foundation/flower/tree/iog-ray-cluster-2.30.0).

From VSCode on your [IOG Ray Cluster](https://cloud.io.net/), set up authentication header once:

```bash
export RAY_JOB_HEADERS="{\"Authorization\": \"Basic $(echo -n ':'$PASSWORD_ENV | base64)\"}"
```

Submit your Flower simulation job:

```bash
ray job submit \
--runtime-env-json '{"working_dir": ".", "pip": "requirements-iog.txt"}' \
-- flwr run . simulation-gpu-1000 --run-config "num-server-rounds=5"
```

For base conda env:

```bash
ray job submit \
--runtime-env-json '{"working_dir": ".", "conda": "conda-env-iog.yml"}' \
-- flwr run . simulation-gpu-1000 --run-config "num-server-rounds=5"
```

To turn on the `FLWR_SUPRESS_DEPRECATION_WARNINGS` flag:

```bash
ray job submit \
--runtime-env-json '{"working_dir": ".", "conda": "conda-env-iog.yml"}' \
-- FLWR_SUPRESS_DEPRECATION_WARNINGS=true flwr run . simulation-gpu-1000 --run-config "num-server-rounds=5"
```

## Troubleshooting

- **Version mismatch errors**: Ensure Ray versions match exactly between your local and cluster environments.
- **Dependency errors (IOG cluster)**: Verify you're using the correct customized Flower version (`iog-ray-cluster-2.30.0`).

---

## Contributions

This repository welcomes contributions. Open an issue or PR if you have suggestions or improvements.
