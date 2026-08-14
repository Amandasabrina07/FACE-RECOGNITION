# Contributing

Contributions should preserve the privacy-first structure of this repository.

## Requirements

- Do not commit real face datasets.
- Do not commit trained biometric models.
- Do not commit Wi-Fi credentials or private network configuration.
- Keep configuration portable and avoid user-specific absolute paths.
- Prefer small, focused pull requests.
- Document behavior changes in the README when they affect setup or usage.

## Basic Check

Before committing Python changes:

```bash
python -m compileall src
```

If you have the required dependencies installed, also run:

```bash
python src/validate_dataset.py
```
