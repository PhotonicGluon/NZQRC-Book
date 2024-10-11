FROM qmcgaw/latexdevcontainer:latest

# Install python cand its related dependencies
RUN apt-get update -y
RUN apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    python3-venv

# Install Manim-related dependencies
RUN apt-get install -y \
    libcairo2-dev \
    libpango1.0-dev \
    ffmpeg \
    dvisvgm

# Install poetry
RUN pip install poetry --break-system-packages

# Install needed packages
RUN tlmgr update --self
COPY . .
RUN tlmgr install `cat latex-packages.txt`
RUN texhash

# Set up workspace
WORKDIR /workspace
