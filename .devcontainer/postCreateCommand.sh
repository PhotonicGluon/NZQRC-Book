#!/bin/bash

# Set up poetry
echo "export PYTHON_PATH='$PYTHON_PATH:$PWD'" >> ~/.zshrc
poetry install --directory=image-generation

export temporary=$(cd image-generation && poetry env info --path)
echo "export PATH='$temporary/bin:$PATH'" >> ~/.zshrc

# Set up aliases
echo "alias porun='poetry run'" >> ~/.zshrc
echo "alias ipynb='porun jupyter notebook --allow-root'" >> ~/.zshrc
echo "alias ipylab='porun jupyter lab --allow-root'" >> ~/.zshrc
