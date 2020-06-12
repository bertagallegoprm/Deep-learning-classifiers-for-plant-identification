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

The data is available at the [Global Biodiversity Information Facility (GBIF) website](https://www.gbif.org/) and it can be dowloaded using its [API](https://www.gbif.org/developer/summary).

The filter for the download of the images and the geographical data must be configured separately.

### Filter configuration

The data download is filtered in basis of a **list of species** and several **parameters used as a filter in the API request**. They must be all configured into a CSV where the first column corresponds to the species names and the rest of the columns to the data request parameters. The filters considered are shown below. For more details see the API documentation.

Custom filters:

- Species names: must be an accepted species binomial name (Genus species).
- search_name: a custom name to identify the search.

API filters:

- media_type: eg.: "StillImage" for images.
- country: eg.: "GB" for United Kingdom.
- has_coordinate: True / False
- kingdom: eg.:"Plantae" 
- basis_of_record: eg.: "PRESERVED_SPECIMEN"
- institution_code: eg.: "K" for RBG Kew.
- limit: eg.: 500. Default is 20 records per occurrence.

There is an example of the filter configuration for the images and the geographical data download in `data/sample_inputs/`.

### Image download


- Run from the main directory (tfm):

```
python3 -m data.geodata.images.image_request.image_request [data/sample_inputs/image_filter.csv]
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


### Geographical data download


- Run from the main directory (tfm):

```
python3 -m data.geodata.request.geodata_request [data/sample_inputs/geodata_filter.csv]
```

- Output:

    - Two files are created in `data/geodata/request/outputs` folder: 

        - a CSV file with the taxon key, occurrence key and the data associated (of interest for the classification: geographical and date). 
        - a text file with the filter applied to the search (input list of species and request parameters). 


## Image pre-processing

### Structure images directory

After downloading the data, copy the selected images dataset into a new folder: `data/images/raw_images`.

- Split the images into train, validation and test dataset (60:20:20):
```
python3 -m data.images.split_image_dataset
```
