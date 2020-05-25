# TFM 

## Getting started

### Set up the working directory (Ubuntu)

I am using `pip` and `virtualenv` to create a virtual environment and manage the dependencies.


- Clone the repo from GitHub: 
```buildoutcfg
git clone -b master https://github.com/bertagallegoprm/tfm.git
```

> Add remote branches if required `git checkout -b branch-name origin/branch-name`

You will need to have installed `pip` and `virtualenv` to create the virtual environment (more information here: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

- Install pip for python3 (if required):
```buildoutcfg
sudo apt install python3-pip
```

- Install python-dev, virtualenv and venv (if required):

```
sudo apt-get install python-dev
```

```
pip3.7 install virtualenv
```

```
sudo apt-get install python3.7-venv
```

- Create a virtual environment (here called "env").
```
python3 -m venv env
```

- Activate the environment:
```
source env/bin/activate
```
> To deactivate the environment run: `deactivate`. 

- To install the packages from `requirements.txt`:

```
pip3 install -r requirements.txt
```

If `tensorflow` installation from `requirements.txt` fails, try (fromhttps://www.tensorflow.org/install/pip):
```
pip install --upgrade tensorflow
```
And test if installed:
```
python -c "import tensorflow as tf;print(tf.reduce_sum(tf.random.normal([1000, 1000])))"
```

- To plot the model architecture an aditional library (`GraphViz`) is needed at the system level. Install it outside the virtual environment:

```
sudo apt-get install graphviz
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

- Split the images into train, validation and test dataset (60:20:20):
```
python3 -m data.images.split_image_dataset
```
