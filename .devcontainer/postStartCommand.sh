# Set up execution permissions for pre- and post- commit hooks
ln -sf ../../.devcontainer/hooks/pre-commit.sh .git/hooks/pre-commit
ln -sf ../../.devcontainer/hooks/post-commit.sh .git/hooks/post-commit
chmod +x /workspace/.git/hooks/pre-commit /workspace/.git/hooks/post-commit
