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

## Data download

The data is available at the [Global Biodiversity Information Facility (GBIF) website](https://www.gbif.org/). 

It can be dowloaded using the [GBIF API](https://www.gbif.org/developer/summary). Here I use the Python [`requests` library](https://requests.readthedocs.io/en/master/).

The images and the rest of the data are downloaded separately. 

### Image download

- Open `data/images/image_request/image_request.py` and customize search filters. I create a local copy of the file: `working_data_request.py` to iterate through filters without modifying the script in the repository.:

    - Search name.
    - API search filters.
    - Input species.


- Run from the main directory (tfm):

```
python3 -m data.images.image_request.image_request 
```


- Output:

    - Images from each species occurrence are downloaded in the `data/images/image_request/images` folder with the following nomenclature: `taxonKey_occurrenceKey.jpg`.

    - Two files are created in `data/images/image_request/request_reports` folder: 

        - a CSV file with the taxon key and occurrence key associated to each occurrece and a flag to know if the image has been downloaded successfully. 
        - a text file with the filter applied to the search (input list of species and request parameters). 

- Get summary of results:

```
python3 -m data.images.image_request.image_request_summary

```
   Output: a CVS file in the `data/images/image_request/image_request/request_results` folder with the number of occurrences and images downloaded per species. 
   
   To print in the terminal a count of the totals in the summary table run: `python3 -m data.images.image_request.image_request_summary_totals`

### Occurrence data download

- Open `geodata/geodata_request.py` and customize search filters. I create a local copy of the file: `working_geodata_request.py` to iterate through filters without modifying the script in the repository.:

    - Search name.
    - API search filters.
    - Input species.


- Run from the main directory (tfm):

```
python3 -m data.geodata.geodata_request 
```

- Output:

    - Two files are created in `data/geodata/request_reports` folder: 

        - a CSV file with the taxon key, occurrence key and the data associated (of interest for the classification: geographical and date). 
        - a text file with the filter applied to the search (input list of species and request parameters). 


## Image pre-processing

### Structure images directory

After downloading the data, copy the selected images dataset into a new folder: `data/images/raw_images`.

- Split the images into train and test dataset (80:20 proportion):
```
python3 -m data.images.split_train_test
```
