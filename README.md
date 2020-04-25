# TFM 

## Getting started

### Set up the working directory (linux)

I am using `pipenv` to create a virtual environment and manage the dependencies.


- Clone the repo from GitHub: 
```buildoutcfg
git clone -b master https://github.com/bertagallegoprm/tfm.git
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

### Run

To run from the terminal, in the file directory:

```
pipenv run python your-python-file.py 
```

## Data 

The data is available at the [Global Biodiversity Information Facility (GBIF) website](https://www.gbif.org/). 

It can be dowloaded using the [GBIF API](https://www.gbif.org/developer/summary). Here I use the Python [`requests` library](https://requests.readthedocs.io/en/master/).

### Image download

- Open `data_request.py` and customize search filters with:

    - Search name.
    - API search filters.
    - Input species.

- I create a local copy of `data_request.py` (`working_data_request.py`) to iterate through filters without modifying the script in the repository.

- Run from the `data` directory:

```
pipenv run python data_request.py 
```

- Output:

    - Images from each species occurrence are downloaded in the `data/image` folder with the following nomenclature: `taxonKey_occurrenceKey.jpg`.

    - Two files are created in `data/request_reports` folder: 

        - a CSV file with the taxon key and occurrence key associated to each occurrece and a flag to know if the image has been downloaded successfully. 
        - a text file with the filter applied to the search (input list of species and request parameters). 