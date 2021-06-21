# scp-author-page

Scripts to automatically generate my author page from static data.

Requires Python 3.7+. Available under the terms of the MIT License.

## Setup

```sh
$ pip install -r requirements.txt
```

Also install `requirements-dev.txt` if developing. All Python code should be formatted with [black](https://github.com/psf/black).

## Linting

```sh
$ black authorpage  # Format source code
$ pylint authorpage  # Check source code
```

## Usage

```sh
$ python -m authorpage <directory...>
```

For instance:

```sh
$ python -m authorpage scp
```

Which will generate its output file at `scp/output.ftml`.
