import os
import subprocess

BOOK_DIR = "book"
COMMIT_TEMPLATE = "code/commit/commit.tex.template"


def get_commit_hash(length: int = 8) -> str:
    """
    Get the short commit hash of the current commit.

    Args:
        length: length of the commit hash to return.

    Returns:
        str: The short commit hash.
    """

    output = subprocess.run(
        ["git", "rev-parse", f"--short={length}", "HEAd"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    output.check_returncode()
    return output.stdout.strip()


def main():
    # Get current commit hash
    commit_hash = get_commit_hash()

    # Replace the commit hash in the template
    with open(COMMIT_TEMPLATE, "r") as f:
        commit_tex = f.read()
        commit_tex = commit_tex.replace("COMMIT_HASH", commit_hash)

    with open(os.path.join(BOOK_DIR, "commit.tex"), "w") as f:
        f.write(commit_tex)


if __name__ == "__main__":
    main()
