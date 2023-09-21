import requests
import sys

# fetch data name
if len(sys.argv) > 1 and isinstance(sys.argv, str):
    radiomics_file = sys.argv[1]
    clin_file = sys.argv[2]
else:
    radiomics_file = input("Enter the radiomics file name (without .csv extension): ")
    clin_file = input("Enter the clinical file name (without .csv extension): ")

# ensure it does not have .csv in its name
if ".csv" in radiomics_file:
    radiomics_file = radiomics_file[:radiomics_file.rfind(".csv")]
# ensure it does not have .csv in its name
if ".csv" in clin_file:
    clin_file = clin_file[:clin_file.rfind(".csv")]

endpoint = "http://rdf-store:7200/repositories/userRepo/statements"

# adding two new nodes in the radiomics graph (clinical and dicom)

queryclinical = f"""

    PREFIX db: <http://data.local/rdf/ontology/>
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX lidicom: <https://johanvansoest.nl/ontologies/LinkedDicom/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    INSERT
        {{

        GRAPH <http://annotations_updated/>
        {{

         db:{radiomics_file}.clinical rdf:type owl:Class.

         db:{radiomics_file}.clinical dbo:table db:{radiomics_file}.

         db:{radiomics_file}.dicom rdf:type owl:Class.

         db:{radiomics_file}.dicom dbo:table db:{radiomics_file}.

         ?patient dbo:has_clinical_features ?clinical.

         ?patient dbo:has_dicom_headers ?dicom.

         ?clinical rdf:type db:{radiomics_file}.clinical.

         ?dicom rdf:type db:{radiomics_file}.dicom.

    }}
    }}
    where
    {{
        BIND(IRI(CONCAT(str(?patient), "/clinical")) as ?clinical).

        BIND(IRI(CONCAT(str(?patient), "/dicom")) as ?dicom).

        ?patient rdf:type db:{radiomics_file}.

    }}

"""

# query for new predicates and equivalencies from NCIT and ROO for radiomic data
queryequiv = f"""

PREFIX db: <http://data.local/rdf/ontology/>
PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
PREFIX lidicom: <https://johanvansoest.nl/ontologies/LinkedDicom/>
PREFIX roo: <http://www.cancerdata.org/roo/>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
INSERT
    {{
    GRAPH <http://annotations_updated/>
    {{

     #replace the predicate dbo:has_column for each table row instance --> column instance with new predicates

     ##Subject label from radiomics file

     ?patient roo:P100061 ?Subject_label.   #has_identifier

     ?patient roo:has_roi_label ?ROI.  ##CHANGE IT

     ?patient roo:P100305 ?sop_uid.  #has_sop_uid


     #study and series from DICOM are mapped under the new class DiCOM

     ?dicom dbo:has_patient ?patient_dicom.


     #clinical features mapped under the new class Clinical

     ?clinical dbo:has_table ?clinical_table.   #has_clinical_table


     #set new equivalencies for the classes

     db:{radiomics_file} owl:equivalentClass ncit:C16960.

     db:{radiomics_file}.research_subject_uid owl:equivalentClass ncit:C25364.

     db:{radiomics_file}.rtstruct_sop_inst_uid owl:equivalentClass ncit:C69219.

     db:{radiomics_file}.roi_human_readable_label owl:equivalentClass ncit:C85402.

    }}
    }}

    where

    {{

    ?patient rdf:type db:{radiomics_file}.

    ?patient dbo:has_column ?Subject_label, ?ROI, ?sop_uid.

    ?patient dbo:has_clinical_features ?clinical.

    ?patient dbo:has_dicom_headers ?dicom.

    ?clinical rdf:type db:{radiomics_file}.clinical.

    ?dicom rdf:type db:{radiomics_file}.dicom.

    ?Subject_label rdf:type db:{radiomics_file}.research_subject_uid.

    ?ROI rdf:type db:{radiomics_file}.roi_human_readable_label.

    ?sop_uid rdf:type db:{radiomics_file}.rtstruct_sop_inst_uid.

    ?Subject_label dbo:has_cell ?radiomiccell.

    ?radiomiccell dbo:has_value ?radiomicID.

    ?ROI dbo:has_cell ?ROIcell.

    ?ROIcell dbo:has_value ?ROIvalue_rad.

    ?sop_uid dbo:has_cell ?sop_uid_cell.

    ?sop_uid_cell dbo:has_value ?sop_uid_value.


    ?clinical_table rdf:type db:{clin_file}.

    ?clinical_table roo:P100061 ?patientID.

    ?patientID rdf:type db:{clin_file}.Patient_\#.

    ?patientID dbo:has_cell ?idcell.

    ?idcell dbo:has_value ?idvalue.

    FILTER (?idvalue = ?radiomicID). #binding radiomic and clinical features using the ID values


    ?patient_dicom rdf:type lidicom:Patient.

    ?patient_dicom lidicom:T00100020 ?dicomID.

    FILTER (?dicomID = ?radiomicID). #binding radiomic and DICOM features using the ID values

    ?ssrsi lidicom:T30060026 ?ROIname. # Structure_Set_ROI_Sequence_Item.

    FILTER (?ROIname = ?ROIvalue_rad). #match GTV names

    ##change to match series UIDs

    #FILTER (?rtstruct_UID = ?sop_uid_value). #match series UIDs names
}}

"""


# call this function to run a query on your endpoint
def runQuery(endpoint, query):
    annotationResponse = requests.post(endpoint,
                                       data="update=" + query,
                                       headers={
                                           "Content-Type": "application/x-www-form-urlencoded",
                                           # "Accept": "application/json"
                                       })
    output = annotationResponse.status_code

    if output == 204:
        print("Mapping added successfully")
    else:
        print("Mapping incorrect")


runQuery(endpoint, queryclinical)
runQuery(endpoint, queryequiv)
