from cleanup.src import remove_pdftex_comments, strip_trailing_whitespace

BOOK_DIRECTORY = "../../book"

print("=" * 50)
print("Stripping trailing whitespace from files.".upper())
print("=" * 50)
strip_trailing_whitespace(BOOK_DIRECTORY)
print()

print("=" * 50)
print("Removing PDFTEX Comments".upper())
print("=" * 50)
remove_pdftex_comments(BOOK_DIRECTORY)
print()

print("Done!")
