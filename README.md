# Build OrbStack Machines

## Introduction

Quickly setup and deploy a full stack of Ordastack machines using the `ordastack` command line tool.

## Prerequisites

- OrbStack Installed <https://orbstack.dev/>
- Poetry installed (recommended) <https://python-poetry.org/>
- Python 3.10 or later

## Quickstart

Creates a ubuntu machine with default settings:

Install the dependencies using poetry:

```bash
poetry install
```

Run the `ordastack` cli commands using fabric commands to build the stack:

```bash
poetry run fab build
```

## Usage

There are a few fabric commands that can be used to manage the stack.

### Build

Builds the stack using the `ordastack` cli tool.

```bash
poetry run fab build
```

### Destroy

Destroys the stack using the `ordastack` cli tool.

```bash
poetry run fab destroy
```

### Start

Starts the stack using the `ordastack` cli tool.

```bash
poetry run fab start
```

### Stop

Stops the stack using the `ordastack` cli tool.

```bash
poetry run fab stop
```

*To avoid typing `poetry run` before every command, you can use the `poetry shell` command to enter a shell with the poetry environment activated.*
