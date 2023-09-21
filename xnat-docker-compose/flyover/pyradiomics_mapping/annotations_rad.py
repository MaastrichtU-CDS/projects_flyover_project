import requests
import pandas as pd
import sys

# fetch data name
if len(sys.argv) > 1 and isinstance(sys.argv[1], str):
    filename = sys.argv[1]
else:
    filename = input("Please provide the filename of the CSV file that was triplified (without .csv extension):\n")

# ensure it does not have .csv in its name
if ".csv" in filename:
    filename = filename[:filename.rfind(".csv")]

endpoint = "http://rdf-store:7200/repositories/userRepo/statements"

#query for new predicates and equivalencies from RO and ROO for radiomic data
def rad(ibsi, pyradiomicfeature, roCode, ftype):
    queryequiv_rad = f"""
        PREFIX db: <http://data.local/rdf/ontology/>
        PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
        PREFIX lidicom: <https://johanvansoest.nl/ontologies/LinkedDicom/>
        PREFIX roo: <http://www.cancerdata.org/roo/>
        PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX ro: <http://www.radiomics.org/RO/>
        INSERT
            {{
                GRAPH <http://annotations_rad/>
                {{

                 #replace the predicate dbo:has_column from radiomic graph for each table row instance --> column instance with new predicates

                 ?patient ro:P00088 ?feature. # has_radiomic_feature

                 ?featureClass owl:equivalentClass ?URICode.

                 ?featureClass dbo:ibsi ?ibsi.

                 ?featureClass dbo:ftype ?ftype.

                 }}

            }}

            WHERE {{

                BIND("%s"^^xsd:string AS ?ibsi).

                BIND("%s"^^xsd:string AS ?pyradiomicfeature).

                BIND("%s"^^xsd:string AS ?roCode).

                BIND("%s"^^xsd:string AS ?ftype).

                BIND(IRI(CONCAT("http://www.radiomics.org/RO/", strafter(str(?roCode), "ro:"))) as ?URICode).

                ?patient rdf:type db:{filename}.

                ?patient dbo:has_column ?feature.

                ?feature rdf:type ?featureClass.

                #FILTER REGEX(str(?featureClass), "original").

                #FILTER REGEX(str(?featureClass), str(?pyradiomicfeature)).

                #CHANGE THE URI EVERYTIME

                BIND(concat("http://data.local/rdf/ontology/{filename}.",?pyradiomicfeature) AS ?pyrad)

                FILTER (str(?featureClass) = str(?pyrad)).
            }}

            """ % (ibsi, pyradiomicfeature, roCode, ftype)

    annotationResponse = requests.post(endpoint,
                               data="update=" + queryequiv_rad,
                               headers={
                                   "Content-Type": "application/x-www-form-urlencoded"
                               })
    output = annotationResponse.status_code

    if output == 204:
        print("Mapping added successfully")
    else:
        print("Mapping incorrect")


df_ft = pd.read_csv('/home/jovyan/work/flyover/pyradiomics_mapping/Final_feature_table.csv')
for row in df_ft.iterrows():
    rad(row[1]['IBSI_Feature_Name'], row[1]['Pyradiomics_Stem_Name'], row[1]['Ontology Concept'], row[1]['Feature type'])

