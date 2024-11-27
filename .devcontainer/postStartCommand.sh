# Ensure that a `commit.tex` file exists
touch book/commit.tex

# Copy Git commit hooks and set their permissions
cp /workspace/.devcontainer/hooks/pre-commit.sh /workspace/.git/hooks/pre-commit
cp /workspace/.devcontainer/hooks/post-commit.sh /workspace/.git/hooks/post-commit
chmod +x /workspace/.git/hooks/pre-commit /workspace/.git/hooks/post-commit
