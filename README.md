# Datasets and Preprocessing for Discourse Data

This is a helper tool for [discopy](https://github.com/MaximilianKr/discopy).

Only tested on Linux (Ubuntu / WSL) so far.

## Setup

Clone the repository first.

```bash
git clone https://github.com/MaximilianKr/discopy-data.git
cd discopy-data
```

### Python 3.8

The legacy code relies on **Python 3.8**. You can install different Python interpreters in parallel (to your system Python) using [pyenv](https://github.com/pyenv/pyenv).

```bash
curl -fsSL https://pyenv.run | bash
```

```bash
pyenv install 3.8.18
```

This step sets Python 3.8 as the default Python interpreter for the local repo.

```bash
pyenv local 3.8.18
```

### Environment Setup

Recommended: use [uv package manager](https://docs.astral.sh/uv/).

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

This should use the previously set up Python 3.8 interpreter.

```bash
uv venv --python 3.8
```

```bash
source .venv/bin/activate
```

```bash
uv pip install --upgrade pip
```

Finally, install `discopy-data`.

```bash
uv pip install -e .
```

---

Instructions beyond this point are from the [original repo](https://github.com/rknaebel/discopy).

## Usage

*Discopy-data* is the discopy backend that handles datastructures, preprocessing, and dataset extraction.

### Sample preparation of a text file, adds also constituent parse trees

The first script uses trankit for tokenization, tagging, and dependency parsing.
In addition, the second script is used, to add constituency trees with the supar parser.
If dependency trees should be added by super as well, add the flag `-d`.

```bash
discopy-tokenize -i /some/examples/wsj_0336 | discopy-add-parses -c
```

### Tokenize raw text without tagging nor parsing

This might be useful for neural pipeline that does not rely on language features.

```bash
cat /some/text | discopy-tokenize --tokenize-only
```

### Preparation of full datasets

This is still experimental. A list of possible datasets is listed under `cli/extract.py`.

```bash
discopy-extract pdtb /data/discourse/conll2016/ --use-gpu --limit 2 | discopy-add-annotations pdtb /data/discourse/conll2016/ --simple-connectives --sense-level 2 | discopy-update-parses --dependency-parser
```
