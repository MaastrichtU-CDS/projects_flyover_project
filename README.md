# FLYOVER

## Introduction


## Workflow

### Data

Demonstration data (HN1) - RADIOMICS-HN1 clinical data accessed from The Cancer Imaging Archive and downloaded on 12 April 2021. For this demonstration, we converted the data into a series of insert commands to populate a PostGreSQL database. The data insert commands to create the PostGreSQL database object are given here.

Demonstration data (HEAD-NECK) - HEAD-NECK-PET-CT clinical data accessed from The Cancer Imaging Archive and downloaded on 12 April 2021. The tabs of the excel spreadsheet were exported as CSV and then concatenated together with the common header row. For this demonstration, we converted the data into a series of insert commands to populate a PostGreSQL database. The data insert commands to create the PostGreSQL database object are given here.

Demonstration data (HNSCC) - HNSCC collection of clinical data was accessed from The Cancer Imaging Archive and downloaded on 12 April 2021. For this demonstration, we converted the data into a series of insert commands to populate a PostGreSQL database. The data insert commands to create the PostGreSQL database object are given here.

Demonstration data (OPC) - OPC-RADIOMICS clinical data accessed from The Cancer Imaging Archive and downloaded on 12 April 2021. For this demonstration, we converted the data into a series of insert commands to populate a PostGreSQL database. The data insert commands to create the PostGreSQL database object are given here.



### Data Descriptor Module

A simple graphical interface tool for helping a local user to describe the data is provided in ./data-descriptor/main.py. First, check the dependencies and install the required libraries using pip and the requirements file :

pip install -r requirements.txt

It is recommended that you execute the script - main.py - using the PyCharm IDE, for example the free Community Edition can be obtained from here : https://www.jetbrains.com/pycharm/download/

In the javaTools subdirectory, there is a Java archive (jar) file that contains the application to parse an entire structured table as a simple flattened Resource Descriptor Format (RDF) object. The so-called "Triplifier" tool works with PostGreSQL and CSV tables, however for the current demonstration we only point it towards CSV input objects.

The end result of the main.py process in the Data Descriptor module is :

1) An ontology (OWL) file that describes the schema of the structured data but does not contain any data elements in itself.

2) A Turtle RDF (TTL) file that contains the data elements in term subject-predicate-object sentences

3) A JSON file containing the selections and annotations entered by the user through the simple graphical user interface.



### Publishing anonyous METADATA



### Data Annotation



### FAIR Data Dashboard Module


## How to run?
Clone the repository (or download) on your machine. On **windows** please use the WSL2 with Docker, on **macOS/Linux**, you can use docker directly.

To execute the complete workflow, please execute the following commands:
```
docker-compose up -d
```

Afterwards you can find the following systems:
* Postgres web admin: [[http://localhost/]]
* RDF repository: [[http://localhost:7200]]




