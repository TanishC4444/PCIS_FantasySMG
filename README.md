# PCIS Fantasy Stock Market Game

A Flask-based educational paper-trading application that lets students practice investing with virtual money.

## Overview

PCIS Fantasy Stock Market Game provides a risk-free environment for learning portfolio management, market dynamics, and trading decisions. The application uses Flask/Jinja for the web layer and local CSV/text files for its current persistence model.

## Features

- User registration and authentication
- Virtual cash and stock positions
- Buy and sell workflows
- Portfolio and transaction tracking
- Market-data integration
- Educational financial-literacy workflow

## Prerequisites

- Python 3
- pip
- Internet access when the configured market-data integration requires it

## Installation

```bash
git clone https://github.com/TanishC4444/PCIS_FantasySMG.git
cd PCIS_FantasySMG
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r req.txt
```

## Quick Start

```bash
python app.py
```

Open the local address printed by Flask.

## Project Structure

```text
PCIS_FantasySMG/
├── app.py
├── index.html
├── templates/
├── req.txt
├── test.py
├── users.csv
├── sold.csv
└── balance.txt
```

## Data and Security

The current implementation uses local files for application state. Do not commit real credentials or private user information. File-based persistence is suitable for development and classroom experimentation but requires stronger concurrency and access controls for production use.

## Testing

```bash
python test.py
```

## Status

Active educational project.

## License

No separate license is currently specified in the repository.

## Support

Use GitHub Issues for questions, bugs, and feature requests.
