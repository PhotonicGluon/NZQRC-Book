#!/bin/bash

# Set up poetry
echo "\n# Path Setup" >> ~/.zshrc

echo "export PYTHON_PATH='$PYTHON_PATH:$PWD'" >> ~/.zshrc
poetry install --directory=code

export temporary=$(cd code && poetry env info --path)
echo "export PATH='$temporary/bin:$PATH'" >> ~/.zshrc

# Fix weird ZSH history file issue
echo "\n# ZSH History Setup" >> ~/.zshrc
echo "HISTFILE=~/.histfile" >> ~/.zshrc
echo "HISTSIZE=1000" >> ~/.zshrc
echo "SAVEHIST=1000" >> ~/.zshrc
echo "setopt appendhistory" >> ~/.zshrc

# Set up aliases
echo "\n# Aliases" >> ~/.zshrc

echo "alias porun='poetry run'" >> ~/.zshrc
echo "alias ipynb='porun jupyter notebook --allow-root'" >> ~/.zshrc
echo "alias ipylab='porun jupyter lab --allow-root'" >> ~/.zshrc

# Misc
echo "\n# Miscellaneous" >> ~/.zshrc
echo "cd code" >> ~/.zshrc
