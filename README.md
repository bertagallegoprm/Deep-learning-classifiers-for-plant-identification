

## Set up the working directory (linux)

I am using `pipenv` to create a virtual environment and manage the dependencies.


- Clone the repo from GitHub: 
```buildoutcfg
git clone -b development https://github.com/bertagallegoprm/tfm.git
```

> Add remote branches if required `git checkout -b branch-name origin/branch-name`

You will need to have installed `pip` and `pipenv` to create the virtual environment (read more about `pipenv` [here](https://pipenv-fork.readthedocs.io/en/latest/)):

- Install pip (if required):
```buildoutcfg
sudo apt install python3-pip
```

- Install pipenv (if required):
```buildoutcfg
pip3 install --user pipenv
```

- To install the packages from `Pipfile`:

```buildoutcfg
pipenv install
```

## Run

To run from the terminal, in the file directory:

```
pipenv run python your-python-file.py 
```