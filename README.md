<h1 align="center">PyNetworkD3</h1>

<p align="center">
    <em>
        Create D3 visualization networks with Python
    </em>
</p>

<p align="center">
<a target="_blank" href="https://colab.research.google.com/drive/1AwtW-FDAaTh_RMBKj4CJYcyKP2xnOanK?usp=sharing"><img src="https://img.shields.io/badge/example-Open%20in%20colab-hsl(30%2C%20100%25%2C%2048%25)?logo=googlecolab" /></a>

<a href="https://pypi.org/project/pynetworkd3/" target="_blank">
    <img src="https://img.shields.io/pypi/v/pynetworkd3?label=version&logo=python&logoColor=%23fff&color=306b9c" alt="PyPI - Version">
</a>

<a href="https://github.com/hernan4444/pynetworkd3/actions?query=workflow%3Atests" target="_blank">
    <img src="https://img.shields.io/github/workflow/status/hernan4444/pynetworkd3/tests?label=tests&logo=python&logoColor=%23fff" alt="Tests">
</a>

<a href="https://github.com/hernan4444/pynetworkd3/actions?query=workflow%3Alinters" target="_blank">
    <img src="https://img.shields.io/github/workflow/status/hernan4444/pynetworkd3/linters?label=linters&logo=github" alt="Linters">
</a> 

<!-- 
<a href="https://codecov.io/gh/daleal/iic2343" target="_blank">
    <img src="https://img.shields.io/codecov/c/gh/daleal/iic2343?label=coverage&logo=codecov&logoColor=ffffff" alt="Coverage">
</a>
-->
</p>

## Installation

Install using `pip`!

```sh
$ pip install pynetworkd3
```

## Input JSON syntax

```
{
    "nodes": [
        {
          "id": "id1",
          "attribute 1": "value attribute 1",
          "attribute 2": "value attribute 2",
          (...)
          "attribute N": "value attribute N",
        },
        {
          "id": "id2",
          "attribute 1": "value attribute 1",
          "attribute 2": "value attribute 2",
          (...)
          "attribute N": "value attribute N",
        },
        (...)
    ],
    "links": [
        {
            "source": "id1",
            "target": "id2",
            "attribute 1": "value attribute 1",
            "attribute 2": "value attribute 2",
            (...)
            "attribute N": "value attribute N",
        },
        (...)
    ]
}
```


## Usage

To use the library, import the `Graph` object directly and use the `export` method
to create a `.html` with the visualization. 


```python
from PyNetworkD3 import Graph

dataset = {
    "nodes": [{"id": 1},{"id": 2},{"id": 3},{"id": 4},{"id": 5}],
    "links": [
        {"source": 1, "target": 3},
        {"source": 2, "target": 3},
        {"source": 1, "target": 3},
        {"source": 5, "target": 3},
        {"source": 4, "target": 1},
    ]
}

graph = Graph(dataset, width=300, height=200, radio=10, tooltip=["id"])

graph.export("output.html)
```

Also you can write the instance in the last line of the notebook's cell (view the <a href="https://colab.research.google.com/drive/1AwtW-FDAaTh_RMBKj4CJYcyKP2xnOanK?usp=sharing"> example in colab</a>) to view the visualization.


## Developing

This library uses `PyTest` as the test suite runner, and `PyLint`, `Flake8`, `Black`, `ISort` and `MyPy` as linters. It also uses `Poetry` as the default package manager.

The library includes a `Makefile` that has every command you need to start developing. If you don't have it, install `Poetry` using:

```sh
make get-poetry
```

Then, create a virtualenv to use throughout the development process, using:

```sh
make build-env
```

Activate the virtualenv using:

```sh
. .venv/bin/activate
```

Deactivate it using:

```sh
deactivate
```

To add a new package, use `Poetry`:

```sh
poetry add <new-package>
```

To run the linters, you can use:

```sh
# The following commands auto-fix the code
make black!
make isort!

# The following commands just review the code
make black
make isort
make flake8
make mypy
make pylint
```

To run the tests, you can use:

```sh
make tests
```

## Releasing

To make a new release of the library, `git switch` to the `master` branch and execute:

```sh
make bump! minor
```

The word `minor` can be replaced with `patch` or `major`, depending on the type of release. The `bump!` command will bump the versions of the library, create a new branch, add and commit the changes. Then, just _merge_ that branch to `master`. Finally, execute a _merge_ to the `stable` branch. Make sure to update the version before merging into `stable`, as `PyPi` will reject packages with duplicated versions. 
