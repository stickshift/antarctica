# Antarctica

Code and analysis supporting Antarctica coding challenge.

## Getting Started

### Prerequisites

* Python 3.12
* UV

### Configure Environment

The following should work from either Bash or ZSH.

```shell
# Configure environment
source environment.sh
make

# Activate venv
source .venv/bin/activate

# Launch jupyter
jupyter lab
```

## Notebooks

The following 3 notebooks walk through my analysis from beginning to end. My final "solution" can be found in the
Summary section of the last notebook.

* [Exploratory Data Analysis](notebooks/01-eda.ipynb)
* [Neighbor Graphs](notebooks/02-neighbor-graphs.ipynb)
* [Probe Clusters](notebooks/03-probe-clusters.ipynb)

## Source Code

The analysis in the notebooks required a number of utility functions for manipulating the data. Most of this code
is implemented in [src/antarctica](src/antarctica) and verified with tests in [tests/unit](tests/unit).