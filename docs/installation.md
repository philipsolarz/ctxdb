# Installation Guide

This guide will walk you through the steps to install and set up the ContextDB Python package.

## Prerequisites

Before you can install ContextDB, you need to have Python 3.6 or later installed on your machine. You can download Python from the official website: https://www.python.org/downloads/

## Installation

You can install ContextDB using pip, which is a package manager for Python.

1. Open a terminal.

2. Install the package with the following command:

```bash
pip install ctxdb
```

## Setup

After installing the package, you need to set up the database connection. This involves specifying the database host, port, username, and password.

You can do this by setting the following environment variables:

- `DB_HOST`: The host of the database.
- `DB_PORT`: The port of the database.
- `DB_USER`: The username to connect to the database.
- `DB_PASSWORD`: The password to connect to the database.

For example, you can set these variables in a bash shell like this:

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_USER=myuser
export DB_PASSWORD=mypassword
```

## Testing the Installation

To verify that ContextDB has been installed correctly, you can run the following command:

```bash
python -c "import ctxdb"
```

If the command does not produce any output, this means that ContextDB has been installed successfully.

## Next Steps

After installing ContextDB, you can start using it to manage and query your context data. For more information on how to use ContextDB, refer to the [Usage Guide](usage.md).