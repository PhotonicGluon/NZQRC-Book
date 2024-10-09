#!/bin/bash

# Set up poetry
echo "export PYTHON_PATH='$PYTHON_PATH:$PWD'" >> ~/.bashrc
poetry install --directory=image-generation

export temporary=$(poetry env info --path)
echo "export PATH='$temporary/bin:$PATH'" >> ~/.bashrc

# Set up aliases
echo "alias porun='poetry run'" >> ~/.bashrc
echo "alias ipynb='porun jupyter notebook --allow-root'" >> ~/.bashrc
echo "alias ipylab='porun jupyter lab --allow-root'" >> ~/.bashrc
