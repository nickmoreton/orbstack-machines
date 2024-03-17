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

If you provide a .env file with the configuration settings, the stack will be built using the settings in the file. See `Build Configuration` below for more information.

## Usage

There are a few fabric commands that can be used to manage the stack.

### Build

Builds the stack using the `ordastack` cli commands.

```bash
poetry run fab build
```

### Destroy

Destroys the stack using the `ordastack` cli commands.

```bash
poetry run fab destroy
```

### Start

Starts the stack using the `ordastack` cli commands.

```bash
poetry run fab start
```

### Stop

Stops the stack using the `ordastack` cli commands.

```bash
poetry run fab stop
```

*To avoid typing `poetry run` before every command, you can use the `poetry shell` command to enter a shell with the poetry environment activated.*

## Build Configuration

Create a file to hold your configuration/command settings in the root of the project. Give it a meaningful name such as `init-mystack`.

Add a sequence of commands to the file to be executed by the `ordastack` cli.

e.g. `init-mystack`:

```shell
#!/bin/bash

# Ubuntu
echo "*** Ubuntu ***"
sudo apt update --yes \
    && sudo apt upgrade --yes --quiet --no-install-recommends \
    && sudo apt install --yes --quiet --no-install-recommends

...
```

Now create a .env file in the root of the project to hold the configuration settings for the stack.

e.g. `.env`:

```shell
MACHINE_NAME=new-ubuntu-machine
MACHINE_SOURCE=ubuntu:mantic
MACHINE_INIT_SCRIPT=init-mystack
```
