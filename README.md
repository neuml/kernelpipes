# Kaggle Kernel Pipelines
kernelpipes is a Python 3.x project that supports running a series of Kaggle kernels through the Kaggle API. 

### Installation
You can use Git to clone the repository from GitHub and install it. It is recommended to do this in a Python Virtual Environment. 

    git clone https://github.com/neuml/kernelpipes.git
    cd kernelpipes
    pip install .

Python 3.6+ is supported

This package assumes a Kaggle token has been generated and installed. See the [kaggle-api](https://github.com/Kaggle/kaggle-api) API credentials section for more information.

### Example
The following YAML script is an example pipeline script. Pipelines require a name and a series of steps to execute. 

```yaml
# Pipeline name
name: CORD-19 Pipeline

# Pipeline execution steps
steps:
  - kernel: davidmezzetti/cord-19-article-entry-dates
  - status: 1m
  - kernel: davidmezzetti/cord-19-analysis-with-sentence-embeddings
  - status: 15m
  - kernel: davidmezzetti/cord-19-risk-factors
  - kernel: davidmezzetti/cord-19-key-scientific-questions
  - status: 1m
  - kernel: davidmezzetti/cord-19-report-builder
  - kernel: davidmezzetti/cord-19-study-metadata-export
  - kernel: davidmezzetti/cord-19-task-csv-exports
  - status: 1m
```

The script above is named "CORD-19 Pipeline" and has a series of sequential steps. Kernel steps will execute a kernel and status steps will poll the status of preceding kernel steps, waiting for completion. For example, the first status command above will run a Status API call every minute checking for completion. If any of the steps return an error status, the pipeline is halted and the program exits. 

Assuming the YAML file above is stored at pipeline.yml, the pipeline can be executed via:

```bash
kernelpipes pipeline.yml
```

### Supported Steps

#### kernel
``` yaml
kernel: /kaggle/kernel/path
```
Returns the kernel specified at /kaggle/kernel/path

### status
```yaml
status: <seconds|s|m|h>
```

Checks the status of preceding kernel steps at the specified duration.

Example durations: 10 for 10 seconds, 30s for 30 seconds, 1m for 1 minute and 1h for 1 hour.
