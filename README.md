# Clinical Summarization Evaluation

Research code for evaluating trustworthiness-enhancement strategies for longitudinal clinical summarization with large language models (LLMs).

The project compares summary-generation and verification workflows over longitudinal clinical notes, with an emphasis on factual support, retrieval quality, temporal consistency, and claim-level evaluation.

## Workflows

The main experiments are implemented as Jupyter notebooks:

| Workflow | Notebook | Purpose |
| --- | --- | --- |
| Data exploration | [`notebooks/direct/01_data_exploration.ipynb`](notebooks/direct/01_data_exploration.ipynb) | Inspect and prepare the clinical data |
| Direct generation | [`notebooks/direct/02_workflow_1_direct_generation_implementation.ipynb`](notebooks/direct/02_workflow_1_direct_generation_implementation.ipynb) | Generate summaries directly from a patient's notes |
| Hierarchical summarization | [`notebooks/hierarchical/01_hierarchical_workflow.ipynb`](notebooks/hierarchical/01_hierarchical_workflow.ipynb) | Summarize notes in multiple stages for long records |
| RAG configuration | [`notebooks/rag/01_configuration_summaries.ipynb`](notebooks/rag/01_configuration_summaries.ipynb) | Configure retrieval and generate RAG summaries |
| RAG evaluation | [`notebooks/rag/02_configuration_evaluation.ipynb`](notebooks/rag/02_configuration_evaluation.ipynb) | Evaluate generated summaries and retrieval configurations |
| RAG implementation | [`notebooks/rag/03_rag_implementation.ipynb`](notebooks/rag/03_rag_implementation.ipynb) | Run the RAG summarization workflow |
| RAG experiments | [`notebooks/experiments/03_workflow_2_rag_experiments.ipynb`](notebooks/experiments/03_workflow_2_rag_experiments.ipynb) | Compare experimental configurations |
| RAG verification | [`notebooks/rag_verification/rag_verification.ipynb`](notebooks/rag_verification/rag_verification.ipynb) | Decompose summaries into claims, retrieve evidence, verify claims, and revise summaries |

## Repository Layout

```text
config/       Configuration and prompt definitions
data/
	raw/        Input CSV files
	processed/  Intermediate claims, embeddings, and checkpoints
	results/    Generated summaries and evaluation outputs
experiments/  Experiment scripts and supporting material
models/       Local embedding model assets
notebooks/    Reproducible exploration and workflow notebooks
paper/        Paper assets and figures
src/
	data/       Data schemas and loading helpers
	evaluation/ Evaluation utilities
	llm/       LLM client and generation helpers
	strategies/ Summarization strategy modules
tests/        Automated tests
```

## Requirements

- Python 3.10 or newer
- Jupyter Notebook or JupyterLab
- Access to the LLM configured by the notebook being run
- Sufficient disk space and memory for the local embedding models in `models/`

The dependency list is in [`requirements.txt`](requirements.txt). The repository also contains local virtual-environment directories in some working copies; these should not be committed or relied on for reproducibility.

## Setup

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Launch Jupyter from the repository root so relative paths resolve correctly:

```bash
jupyter notebook
```

In VS Code, open the repository folder, select the environment's Python interpreter, and run the notebooks in order for the workflow you want to reproduce.

## Environment Variables

The active LLM helper in [`src/llm/llm.py`](src/llm/llm.py) reads:

```bash
export OPENAI_API_KEY="your-api-key"
```

You can place the variable in a local `.env` file instead. Do not commit `.env` or API keys. Several exploratory notebooks also reference provider-specific variables such as `GEMINI_API_KEY`, `HF_TOKEN`, or `GROQ_API_KEY`; define those only when running the corresponding notebook.

## Data and Outputs

The expected raw inputs are stored under [`data/raw/`](data/raw/), including clinical notes, admissions, and patient metadata. Typical generated artifacts are written under:

- [`data/processed/`](data/processed/) for atomic claims, retrieval checkpoints, embeddings, and verification checkpoints
- [`data/results/direct/`](data/results/direct/) for direct-generation outputs
- [`data/results/hierarchical/`](data/results/hierarchical/) for hierarchical outputs
- [`data/results/rag/`](data/results/rag/) for RAG summaries and evaluation results
- [`data/results/rag_verification/`](data/results/rag_verification/) for claim-verification and revised-summary results

Generated files can be large. Checkpoint files should be retained when resuming long-running experiments, and outputs should be inspected before being used in the paper or downstream analysis.

## Recommended Execution Order

1. Run the data exploration notebook and confirm that the raw files load successfully.
2. Run the direct or hierarchical workflow to establish baseline summaries.
3. Run the RAG configuration and implementation notebooks.
4. Run the RAG evaluation and experiment notebooks.
5. Run the RAG verification notebook after RAG summaries and original clinical-note chunks are available.

The verification workflow is checkpoint-oriented. It extracts atomic claims, retrieves original-note evidence, verifies claims, and revises summaries only when unsupported or partially supported claims are found. For a first run, use a small patient subset before running the full dataset.

## Running Tests

From the repository root:

```bash
pytest
```

The notebooks contain additional workflow-level checks and examples that are not all covered by the automated test suite.

## Reproducibility Notes

- Run commands from the repository root unless a notebook explicitly states otherwise.
- Keep the selected Python interpreter and notebook kernel consistent.
- Record the model name, prompt version, retrieval settings, patient subset, and random seed for each experiment.
- Do not treat generated summaries as clinical advice. This repository is for research evaluation, not clinical decision-making.

## License and Data Notice

No project license is currently specified. Add a license before distributing the code outside the research group. Verify that all clinical data, model files, and generated outputs are permitted for the intended use and distribution.