# Image Generation

## Setup

Install the manim dependencies by running

```bash
poetry install --with manim
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

### Moving Generated Images

Run:
```bash
poetry run python image_operations.py transfer_images
```

For doing a dry run before the actual move:

```bash
poetry run python image_operations.py transfer_images --dry-run
```
