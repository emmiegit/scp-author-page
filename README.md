# scp-author-page

Scripts to automatically generate my author page from static data.

Requires Python 3.7+. Available under the terms of the MIT License.

## Setup

```
$ pip install -r requirements.txt
```

Also install `requirements-dev.txt` if developing. All files should be formatted with [black](https://github.com/psf/black).

## Linting

```
$ black authorpage  # Format source code
$ pylint authorpage  # Check source code
```

## Usage

```
$ python -m authorpage <directory...>
```

For instance:

```
$ python -m authorpage scp
```

Which will generate its output file at `scp/output.ftml`.
