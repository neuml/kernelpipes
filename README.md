# Kaggle Kernel Pipelines
kernelpipes is a Python 3.x project that supports running a series of Kaggle kernels through the Kaggle API. 

### Installation
You can install kernelpipes directly from GitHub using pip. Using a Python Virtual Environment is recommended.

    pip install git+https://github.com/neuml/kernelpipes

Python 3.6+ is supported

This package assumes a Kaggle token has been generated and installed. See the [kaggle-api](https://github.com/Kaggle/kaggle-api) API credentials section for more information.

### Example
The following YAML script is an example pipeline script. Pipelines require a name and a series of steps to execute. 

```yaml
# Pipeline name
name: CORD-19 Pipeline

# Schedule job to run every 15 minutes between 10pm - 12am local time
schedule: "*/15 22-23 * * *"

# Pipeline execution steps
steps:
  - check: allen-institute-for-ai/CORD-19-research-challenge
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

Kernels are started until they reach a status step. In the example above, the last status call executes cord-19-report-builder, cord-19-study-metadata-export and cord-19-task-csv-exports in parallel and waits for all 3 to complete. 

Assuming the YAML file above is stored at pipeline.yml, the pipeline can be executed via:

```bash
kernelpipes pipeline.yml
```

### Basic pipeline configuration

#### name
```yaml
name: <pipeline name>
```

Required field, names the pipeline

#### schedule
```yaml
schedule: cron string
```

Optional field to enable running jobs through a scheduler. System cron can be used in place of this, depending on preference. One advantage of this method is that new jobs won't be spawned while a prior job is running. For example if a job is scheduled to run every hour and a run takes 1.5 hours, it will skip the 2nd run and start again on the 3rd hour. 

### Steps

#### check
```yaml
check: /kaggle/dataset/path
```

Allows conditionally running a pipeline based on dataset update status. Retrieves dataset metadata and compares the latest version against the last run version and only allows processing to proceed if the dataset has been updated. If there is no local metadata for the dataset, the run will proceed.

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
