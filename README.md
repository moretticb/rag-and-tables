# RAG and tables

Reproducible materials from the [RAG decomposition blog post](https://www.xebia.com/blog) on how to break down tables into better chunk formats, improving retrieval.

## Setup

Make sure to have poetry installed and install the project dependencies:

```bash
poetry install
```

## Running the experiment

Run `run_experiment.sh`:

```bash
cd experiment
poetry run ./run_experiment.sh
```

It will generate all chunks from the three approaches (decomposition, raw parsing with PyPDF and reverse engineering), calculate the embeddings and generate the final plot for comparisons.

Refer to the contents of `run_experiment.sh` to separately run parts of this process.

