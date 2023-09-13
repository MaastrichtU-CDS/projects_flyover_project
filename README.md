# FLYOVER

## Introduction

A dockerized Data FAIR-ification tool that processes clinical, radiomics and DICOM metadata and converts them into Resource Descriptor Format (RDF).

## Components

### 1. xnat-docker-compose

#### How to run?
Clone the repository (or download) on your machine. On windows please use the WSL2 with Docker, on macOS/Linux, you can use docker directly.
To execute the XNAT workflow, please execute the following commands from the xnat-docker-compose folder:

```
cp default.env .env
```

```
chmod a+x xnat/make*.sh
```

```
chmod a+x xnat/wait*.sh
```

```
docker-compose up -d
```

### Docker compose initiates the following

* Jupyter notebook: [[http://localhost/8881]] (Login password: tomcat-1)
* xnat instance: [[http://localhost:80]]
* xnat db: [[http://localhost:8104]]

### 2. graphdb-docker-compose

#### How to run?

To run a graphdb instance on your machine, please execute the following commands from the graphdb-docker-compose folder:

```
docker-compose up -d
```

### Docker compose initiates the following

* GraphDB instance: [[http://localhost/7200]] 

Depending on your system it could take a few minutes for all the instances to set up. You can check status using the command **docker stats**. Once all five docker images in the XNAT and the Graphdb package are stable at very low load, it probably means everything is up and running nice in the background.

<details><summary>Expand step-by-step instructions for data processing in Jupyter notebook:</summary>


**IMPORTANT: Create a new project in Xnat if it isn't already created**
#### Step 1. Uploading imaging data with python batching script

This can only work with adequately de-identified and correctly-cleaned DICOM data. 

From the work directory /home/jovyan/work/o-raw, run the python notebook script "upload_dicom_bundles_into_xnat.ipynb" to iterate through every patient folder in a local filesystem directory, that will package each patient folder as a zip object, and then transmit the zip via API into your local XNAT docker instance which will collect it and try to archive it.

(Make sure to change the xnat username, password and project name in the script)

#### Step 2. Generating radiomics data

From the work directory /home/jovyan/work/o-raw, run the python notebook "batch_conv_nrrd_xnat-1.ipynb". This converts the RTSTRUCT to NRRD format which is used by the pyRadiomics package for feature extraction.

As the next step, run the notebook script "download_pyradiomics-2.ipynb", which collects the radiomics results from xnat for each of the Dicom file and saves the merged CSV file locally in the same work folder.

#### Step 3. DICOM headers as semantic data

Open a new terminal in the same notebook environment and run the following command to open a Dicom SCP service. We use a "-s" tag in the command so that users can send data to a specific rdf-endpoint.

```
ldcm-scp -s http://rdf-store:7200/repositories/userRepo/statements 104
```

While this SCP server is open and ready, run the notebook script "xnat_to_ldcm_scp-1.ipynb". This sends the Dicom files to this service using storescu commands. On completion, you will find the resultant Dicom triples in the rdf-endpoint running in your machine.

#### Step 4. Radiomics as semantic data

A simple graphical interface tool for structured data conversion (CSV or PostGreSQL) into RDF format is included in this workflow. From the work directory /home/jovyan/work/flyover, run the notebook script for structured data in "user_module.ipynb". 

A web based GUI runs on **port 5000** prompting the user to upload their data. Upload the pyradiomic CSV file here. Triplifier runs and converts this data into RDF triples which is then uploaded to the same rdf endpoint, along with a data specific ontology (OWL) file. 
The next page displays the list of columns and prompts the user to give some basic information about their data which is then added back to the OWL file (Skip this step for the radiomic file as they are already standardized).

#### Step 5. Clinical data as semantic data

Using the same GUI, upload your clinical CSV files for them to be converted to rdf triples and pushed to the same rdf endpoint. Use the interface to provide information about your data columns which can then be used for creating custom annotations for your data.

#### Step 6. Annotation of ROIs

From the same notebook script, run the roi_reader which prompts the user to choose the primary and nodal GTVs for each of their DICOM files. Clicking on submit maps the GTVs to semantic codes from domain ontologies.
</details>

#### Publishing anonymous METADATA
The user can publish their OWL files (which doesn't have patient-specific private data) to a private cloud repository, which can then be used to create a customised annotation graph for their data. The usage of metadata for the creation of annotations ensures the privacy of user data.



