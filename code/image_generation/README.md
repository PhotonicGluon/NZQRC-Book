# Image Generation

## Setup

Install the image generation dependencies by running

```bash
poetry install --with imgen
```

## Main Operations

For all of the following, make sure the commands are running in this folder. You can ensure that by running

```bash
cd code/image-generation
```

### Running Manim Notebook/Lab Server

For running Jupyter notebook with Manim:

```bash
ipynb
```

For running Jupyter lab with Manim:

```bash
ipylab
```

### Trimming Generated Images

Run:

```bash
poetry run python main.py trim -o media/trimmed
```

### Moving Generated Images

Run:
```bash
poetry run python main.py transfer
```

For doing a dry run before the actual move:

```bash
poetry run python main.py transfer --dry-run
```

For moving trimmed images:

```bash
poetry run python main.py transfer --generated-images-folder media/trimmed
```

### Trim and Transfer Images

Run:

```bash
python main.py tat
```

### Do-All

Run:

```bash
poetry run python main.py do-all
```

To generate images for certain part(s):

```bash
# Single part
poetry run python main.py do-all --part 0

# Multiple parts
poetry run python main.py do-all --part 0 --part 1 --part 2
```

To generate images for certain notebook(s):

```bash
# Single notebook
poetry run python main.py do-all --notebook notebook_1_path.ipynb

# Multiple notebooks
poetry run python main.py do-all --notebook notebook_1_path.ipynb --notebook notebook_2_path.ipynb --notebook notebook_3_path.ipynb
```
