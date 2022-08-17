# FLYOVER

## Introduction

We have build a dockerized Data FAIR-ification tool that takes four clinical datasets from the The Cancer Imaging Archive (TCIA) and converts them into Resource Descriptor Format (RDF). This conversion is done by an application which parses an entire structured table as a simple flattened RDF object. This so-called "Triplifier" tool works with PostGreSQL and CSV tables.

An additional layer with annotations (using predefined universal Ontologies) are added for the four RDF triple files, since they have a flat schema and do not yet hold any semantics. Both the triples and the annotations are uploaded to a RDF triple store (GraphDB in our case). The output of this FAIR-ified Linked Data is shown in a Data visualization Dashboard. 

## Data

Demonstration data (HN1) - RADIOMICS-HN1 clinical data accessed from The Cancer Imaging Archive and downloaded on 12 April 2021. For this demonstration, we converted the data into a series of insert commands to populate a PostGreSQL database. The data insert commands to create the PostGreSQL database object are given here.

Demonstration data (HEAD-NECK) - HEAD-NECK-PET-CT clinical data accessed from The Cancer Imaging Archive and downloaded on 12 April 2021. The tabs of the excel spreadsheet were exported as CSV and then concatenated together with the common header row. For this demonstration, we converted the data into a series of insert commands to populate a PostGreSQL database. The data insert commands to create the PostGreSQL database object are given here.

Demonstration data (HNSCC) - HNSCC collection of clinical data was accessed from The Cancer Imaging Archive and downloaded on 12 April 2021. For this demonstration, we converted the data into a series of insert commands to populate a PostGreSQL database. The data insert commands to create the PostGreSQL database object are given here.

Demonstration data (OPC) - OPC-RADIOMICS clinical data accessed from The Cancer Imaging Archive and downloaded on 12 April 2021. For this demonstration, we converted the data into a series of insert commands to populate a PostGreSQL database. The data insert commands to create the PostGreSQL database object are given here.

## 1. FAIR data dashboard

### How to run?

#### Step 1
Clone the repository (or download) on your machine. On **windows** please use the WSL2 with Docker, on **macOS/Linux**, you can use docker directly.

To execute the complete workflow, please execute the following commands from the project folder:
```
docker-compose up -d
```
#### Docker compose initiates the following
1. Docker compose builds a postgres and a pgadmin front end.
2. SQL insert queries immediately fire into Postgres and (if you look in pgAdmin) creates 4 databases, one for each of the four “projects”
3. GraphDB builds locally.
4. FOUR parallel Triplifier projects fire up, one for each of the four clinical “projects”.
5. Triplifier projects exit code upon successful completion.
6. GraphDB now has FOUR rdf repositories, each with two graphs - 
    <<http://data.local/>> with the RDF triples.
    <<http://ontology.local/>> with a data specific ontology.

![]("C:\\Users\\P70070487\\Pictures\\Screenshots\\Screenshot_graph.png")


#### Step 2
Navigate to the annotations folder of the project and execute the command:
```
docker-compose up -d
```
#### Docker compose initiates the following
1. Annotations app builds and adds a new <<http://annotation.local/>> graph in each of the four graphDB repositories. This graph contains semantics for the flat RDF triples from the Triplifier.
2. Finally, the user is able to visualize the data from all the four annotated datasets (now linked together via their semantics) in a dashboard. This dashboard uses SPARQL queries to retrieve the triples from graphDB.

Afterwards you can find the following systems:
* Postgres web admin: [[http://localhost/]]
* RDF repository: [[http://localhost:7200]]
* Data Dashboard: [[http://localhost:8050]]

## Developers

- Varsha Gouthamchand
- Leonard Wee
- Johan van Soest


