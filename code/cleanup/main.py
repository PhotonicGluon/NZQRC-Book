from cleanup.src import strip_trailing_whitespace

BOOK_DIRECTORY = "../../book"

print("=" * 50)
print("Stripping trailing whitespace from files.".upper())
print("=" * 50)
strip_trailing_whitespace(BOOK_DIRECTORY)
print()

print("Done!")
