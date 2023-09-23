# FLYOVER

## Introduction

We have build a dockerized Data FAIR-ification tool that takes clinical datasets and converts them into Resource Descriptor Format (RDF). This conversion is done by an application which parses an entire structured table as a simple flattened RDF object. This so-called "Triplifier" tool works with PostGreSQL and CSV tables.

For user data, a new module (data_descriptor) is created where the user can describe their own data and provide us with the metadata, which can then be used to create annotations.

## Components

1. Data_descriptor (For user data)

### 1. Data Descriptor Module
A simple graphical interface tool for helping a local user to describe their own data (in the form of CSV or PostGreSQL). On uploading the data, Triplifier runs and converts this data into RDF triples which is then uploaded to the RDF store, along with an OWL file. The next page displays the list of columns and prompts the user to give some basic information about their data which is then added back to the OWL file in the RDF store.  

#### How to run?

##### Step 1:
Clone the repository (or download) on your machine. On windows please use the WSL2 with Docker, on macOS/Linux, you can use docker directly.
For the complete workflow, please execute the following commands from the project folder:
```
docker-compose up -d
```

## Docker compose initiates the following

1. Docker compose builds a graphdb and jupyter notebook front end.
2. Running the user_module notebook from jupyter notebook builds a webUI for user to upload their relational database.
3. Triplifier fires up, converts the uploaded database to RDF.
4. Triplifier exits code upon successful completion. The next page lists the columns from the data and requires the user to provide information about the data. 
5. GraphDB now has a rdf repository called userRepo, with two graphs:

- An ontology (OWL) file <http://ontology.local/> that describes the schema of the structured data but does not contain any data elements in itself, along with the selections and annotations entered by the user through the simple graphical user interface.
- A Turtle RDF (TTL) file <http://data.local/> that contains the data elements in term subject-predicate-object sentences.

You can find the following systems:
* Jupyter notebook: [[http://localhost/8881]] (Login password: flyover-1)
* RDF repository: [[http://localhost:7200]]

#### Publishing anonyous METADATA
The user can publish their OWL files to a private cloud repository, which can then be used to create a customised annotation graph for their data. The usage of metadata for the creation of annotations ensures the privacy of user data.

## Developers

- Varsha Gouthamchand
- Leonard Wee
- Johan van Soest


