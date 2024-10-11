# Quick Response

## Setup

Install the QR dependencies by running

```bash
poetry install --with qr
```

## Main Operations

For all of the following, make sure the commands are running in this folder. You can ensure that by running

```bash
cd code/qr
```

### Generating QR Images

Run:

```bash
poetry run python main.py generate 
```

To see all available options:

```bash
poetry run python main.py generate --help
```

### Transferring QR Images

Run:

```bash
poetry run python main.py transfer
```

To see all available options:

```bash
poetry run python main.py transfer --help
```
