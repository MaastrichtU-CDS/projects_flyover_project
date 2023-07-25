import requests
import pandas as pd

endpoint = "http://localhost:7200/repositories/userRepo/statements"

#query to add new classes - (Neoplasm and Radiotherapy) and unit classes for clinical data
queryneoplasm = """
PREFIX db: <http://data.local/rdf/ontology/>
PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
PREFIX lidicom: <https://johanvansoest.nl/ontologies/LinkedDicom/>
PREFIX roo: <http://www.cancerdata.org/roo/>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
INSERT  
    {
    
    GRAPH <http://annotations_updated/>
    {
    
     db:Maastricht.years rdf:type owl:Class.  
   
     db:Maastricht.years rdfs:label "Years".
    
     db:Maastricht.days rdf:type owl:Class.
    
     db:Maastricht.days rdfs:label "Days".
    
     db:Maastricht.Gray rdf:type owl:Class. 
  
     db:Maastricht.Gray rdfs:label "Gy".
   
     db:Maastricht.radiotherapyClass rdf:type owl:Class.
    
     db:Maastricht.radiotherapyClass dbo:table db:Maastricht.
     
     db:Maastricht.neoplasmClass rdf:type owl:Class. 
     
     db:Maastricht.neoplasmClass dbo:table db:Maastricht.
    
     ?patient dbo:has_column ?neoplasm, ?radiotherapy.
    
     ?neoplasm rdf:type db:Maastricht.neoplasmClass.
    
     ?radiotherapy rdf:type db:Maastricht.radiotherapyClass.
  
}
}
where 
{
    BIND(IRI(CONCAT(str(?patient), "/neoplasm")) as ?neoplasm).
    
    BIND(IRI(CONCAT(str(?patient), "/radiotherapy")) as ?radiotherapy).
    
    ?patient rdf:type db:Maastricht.
   
}
"""

queryclinical = """

    PREFIX db: <http://data.local/rdf/ontology/>
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX lidicom: <https://johanvansoest.nl/ontologies/LinkedDicom/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    INSERT  
        {
        
        GRAPH <http://annotations_updated/>
        {
       
         db:plastimatch_version_hn1.clinical rdf:type owl:Class.
        
         db:plastimatch_version_hn1.clinical dbo:table db:plastimatch_version_hn1.

         db:plastimatch_version_hn1.dicom rdf:type owl:Class.
        
         db:plastimatch_version_hn1.dicom dbo:table db:plastimatch_version_hn1.

         ?patient dbo:has_clinical_features ?clinical.

         ?patient dbo:has_dicom_headers ?dicom.
            
         ?clinical rdf:type db:plastimatch_version_hn1.clinical.

         ?dicom rdf:type db:plastimatch_version_hn1.dicom.
        
    }
    }
    where 
    {
        BIND(IRI(CONCAT(str(?patient), "/clinical")) as ?clinical).

        BIND(IRI(CONCAT(str(?patient), "/dicom")) as ?dicom).
        
        ?patient rdf:type db:plastimatch_version_hn1.
       
    }

"""

#query for new predicates and equivalencies from NCIT and ROO for radiomic data
queryequiv = """

PREFIX db: <http://data.local/rdf/ontology/>
PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
PREFIX lidicom: <https://johanvansoest.nl/ontologies/LinkedDicom/>
PREFIX roo: <http://www.cancerdata.org/roo/>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
INSERT  
    {
    GRAPH <http://annotations_updated/>
    {

     #replace the predicate dbo:has_column for each table row instance --> column instance with new predicates

     ##Subject label from radiomics file
        
     ?patient roo:P100061 ?Subject_label.   #has_identifier

     ?patient roo:has_roi_label ?ROI.  ##CHANGE IT

     ?patient roo:P100305 ?sop_uid.  #has_series_uid


     #study and series from DICOM are mapped under the new class DiCOM

     ?dicom dbo:hasStudy ?study.

     ?dicom dbo:T00100020 ?dicomID.

     ?study dbo:hasSeries ?series.

     ?series dbo:T00080060 ?rt.

     ?series dbo:hasImage ?rtstruct.

     ?rtstruct dbo:hasImageID ?rtstruct_UID.

     ?rtstruct dbo:hasStructureSetROI ?ssrs.

     ?ssrs dbo:hasSequenceItem ?b. #Radiotherapy Referenced Series Sequence

     ?b dbo:hasROI ?ROIname.

    
     #clinical features mapped under the new class Clinical

     #?clinical roo:P100061 ?patientID.   #has_identifier
        
     ?clinical roo:P100018 ?gender.      #has_biological_sex
        
     ?clinical roo:P100000 ?age. 

     ?age roo:P100027 db:Maastricht.years.  
        
     ?clinical roo:P100022 ?hpv.         #has_finding
        
     ?clinical roo:P100214 ?asa.         #has_measurement
        
     ?clinical roo:haswhostatus ?whostatus.   #has_WHO_status
        
     ?clinical roo:P100029 ?neoplasm.
   
     ?neoplasm roo:P100244 ?tstage.      #has_T_stage
        
     ?neoplasm roo:P100242 ?nstage.      #has_N_stage
      
     ?neoplasm roo:P100241 ?mstage.      #has_M_stage
            
     ?neoplasm roo:P100219 ?ajcc.        #has_AJCC_stage
        
     ?neoplasm roo:P100202 ?tumour.      #tumourSite
        
     ?neoplasm roo:P10032 ?metastasis.   #has_metastasis
        
     ?neoplasm roo:P100022 ?eventrecurrence, ?eventrecurrencedays, ?localrecurrence, ?localrecurrencedays, ?regionalrecurrence, ?regionalrecurrencedays, ?metastasisdays.  #has_finding
        
     ?localrecurrencedays roo:P100027 db:Maastricht.days.
        
     ?regionalrecurrencedays roo:P100027 db:Maastricht.days.
        
     ?metastasisdays roo:P100027 db:Maastricht.days.
        
     ?clinical roo:P100403 ?radiotherapy. #treated_by 
        
     ?radiotherapy roo:P100027 ?rttotaldays. #has_unit
        
     ?rttotaldays roo:P100027 db:Maastricht.days.
        
     ?radiotherapy roo:P100023 ?graytotaldose. #has_dose
        
     ?graytotaldose roo:P100027 db:Maastricht.Gray.
        
     ?radiotherapy roo:P100214 ?graydoseperfraction.   #has_dose_per_fraction
     
     ?graydoseperfraction roo:P100027 db:Maastricht.Gray.
    
     ?radiotherapy roo:P100224 ?rtfractions. #has_fraction_count
      
     ?clinical roo:P100403 ?surgery.     #treated_by
     
     ?clinical roo:P100028 ?survival.    #has_vital_status 
        
     ?clinical roo:P100026 ?overallsurvivaldays.
        
     ?overallsurvivaldays roo:P100027 db:Maastricht.days.
        
     ?clinical roo:P100231 ?chemo.        #chemo_administered
      

     #set new equivalencies for the classes 

     db:plastimatch_version_hn1 owl:equivalentClass ncit:C16960.

     db:plastimatch_version_hn1.research_subject_uid owl:equivalentClass ncit:C25364.
        
     db:plastimatch_version_hn1.rtstruct_sop_inst_uid owl:equivalentClass ncit:C69219.

     db:plastimatch_version_hn1.ROI_label owl:equivalentClass ncit:C85402.

        
     db:Maastricht owl:equivalentClass ncit:C16960.
        
     db:Maastricht.id owl:equivalentClass ncit:C25364.
        
     db:Maastricht.biological_sex owl:equivalentClass ncit:C28421.
        
     db:Maastricht.age_at_diagnosis owl:equivalentClass roo:C100003.
    
     db:Maastricht.overall_hpv_p16_status owl:equivalentClass ncit:C14226.
        
     db:Maastricht.pretreat_hb_in_mmolperlitre owl:equivalentClass roo:asaScore.
        
     db:Maastricht.performance_status_ecog owl:equivalentClass ncit:C105721.
        
     db:Maastricht.clin_t owl:equivalentClass ncit:C48885.
     
     db:Maastricht.clin_n owl:equivalentClass ncit:C48884.

     db:Maastricht.clin_m owl:equivalentClass ncit:C48883.
        
     db:Maastricht.ajcc_stage owl:equivalentClass ncit:C38027.
        
     db:Maastricht.cancer_surgery_performed owl:equivalentClass ncit:C17173.
      
     db:Maastricht.index_tumour_location owl:equivalentClass ncit:C3263.
    
     db:Maastricht.event_recurrence_metastatic_free_survival owl:equivalentClass roo:eventrecurrence.
    
     db:Maastricht.recurrence_metastatic_free_survival_in_days owl:equivalentClass roo:eventrecurrencedays.
                
     db:Maastricht.event_local_recurrence owl:equivalentClass roo:localrecurrence.

     db:Maastricht.local_recurrence_in_days owl:equivalentClass roo:localrecurrencedays.

     db:Maastricht.event_locoregional_recurrence owl:equivalentClass roo:regionalrecurrence.

     db:Maastricht.locoregional_recurrence_in_days owl:equivalentClass roo:regionalrecurrencedays.
        
     db:Maastricht.event_distant_metastases owl:equivalentClass ncit:C19151.
               
     db:Maastricht.distant_metastases_in_days owl:equivalentClass roo:metastasisdays.
        
     db:Maastricht.event_overall_survival owl:equivalentClass ncit:C25717.

     db:Maastricht.overall_survival_in_days owl:equivalentClass roo:overallsurvivaldays.
        
     db:Maastricht.chemotherapy_given owl:equivalentClass ncit:C15632.
    
     db:Maastricht.radiotherapy_total_treat_time owl:equivalentClass roo:rttotaldays.
    
     db:Maastricht.radiotherapy_refgydose_total_highriskgtv owl:equivalentClass roo:graytotaldose.
        
     db:Maastricht.radiotherapy_refgydose_perfraction_highriskgtv owl:equivalentClass roo:graydoseperfraction.
    
     db:Maastricht.radiotherapy_number_fractions_highriskgtv owl:equivalentClass roo:rttotalfraction.
   
     db:Maastricht.years owl:equivalentClass ncit:C29848.
      
     db:Maastricht.days owl:equivalentClass ncit:C25301. 
    
     db:Maastricht.Gray owl:equivalentClass ncit:C18063.
    
     db:Maastricht.neoplasmClass owl:equivalentClass ncit:C3262.
    
     db:Maastricht.radiotherapyClass owl:equivalentClass ncit:C15313.
     
     dbo:has_value owl:sameAs roo:P100042.    #has_value
    
     dbo:has_unit owl:sameAs roo:P100047.    #has_value
     
     dbo:cell_of rdf:type owl:ObjectProperty;
                 owl:inverseOf dbo:has_cell.

    } 
    }


    where

    {  

    ?patient rdf:type db:plastimatch_version_hn1.
    
    ?patient dbo:has_column ?Subject_label, ?ROI, ?sop_uid.

    ?patient dbo:has_clinical_features ?clinical.

    ?patient dbo:has_dicom_headers ?dicom.

    ?clinical rdf:type db:plastimatch_version_hn1.clinical.

    ?dicom rdf:type db:plastimatch_version_hn1.dicom.

    ?Subject_label rdf:type db:plastimatch_version_hn1.research_subject_uid. 

    ?ROI rdf:type db:plastimatch_version_hn1.ROI_label.

    ?sop_uid rdf:type db:plastimatch_version_hn1.rtstruct_sop_inst_uid. 

    ?Subject_label dbo:has_cell ?radiomiccell.
    
    ?radiomiccell dbo:has_value ?radiomicID.

    ?ROI dbo:has_cell ?ROIcell.
    
    ?ROIcell dbo:has_value ?ROIvalue_rad.

    ?sop_uid dbo:has_cell ?sop_uid_cell.
    
    ?sop_uid_cell dbo:has_value ?sop_uid_value.


    ?patient_clin rdf:type db:Maastricht.

    ?patient_clin dbo:has_column ?patientID, ?gender, ?age, ?tumour, ?whostatus, ?hpv, ?tstage, ?nstage, ?mstage, ?ajcc, ?asa, ?surgery, ?chemo, ?rttotaldays, ?graytotaldose, ?graydoseperfraction, ?survival, ?overallsurvivaldays, ?localrecurrence, ?localrecurrencedays, ?regionalrecurrence, ?regionalrecurrencedays, ?metastasis, ?metastasisdays, ?neoplasm, ?radiotherapy, ?rtfractions, ?eventrecurrence, ?eventrecurrencedays.

    ?patientID rdf:type db:Maastricht.id.

    ?patientID dbo:has_cell ?idcell.

    ?idcell dbo:has_value ?idvalue.
    
    FILTER (?idvalue = ?radiomicID). #binding radiomic and clinical features using the ID values


    ?patient_dicom rdf:type lidicom:Patient.

    ?patient_dicom lidicom:T00100020 ?dicomID.

    FILTER (?dicomID = ?radiomicID). #binding radiomic and DICOM features using the ID values

    ?patient_dicom lidicom:has_study ?study.

    ?study rdf:type lidicom:Study.

    ?study lidicom:has_series ?series.

    ?series rdf:type lidicom:Series.

    ?series lidicom:T00080060 ?rt.

    FILTER regex(str(?rt), ("RTSTRUCT")).

    ?series lidicom:has_image ?rtstruct.

    ?rtstruct rdf:type lidicom:Radiotherapy_Structure_Object.

    ?rtstruct lidicom:T00080018 ?rtstruct_UID.

    ?rtstruct lidicom:T30060020 ?ssrs.

    ?ssrs rdf:type lidicom:Structure_Set_ROI_Sequence.

    ?ssrs lidicom:has_sequence_item ?b. #Radiotherapy Referenced Series Sequence

    ?b rdf:type lidicom:Structure_Set_ROI_Sequence_Item.

    ?b lidicom:T30060026 ?ROIname.

    FILTER (?ROIname = ?ROIvalue_rad). #match GTV names

    FILTER (?rtstruct_UID = ?sop_uid_value). #match series UIDs names


    ?neoplasm rdf:type db:Maastricht.neoplasmClass.
    
    ?radiotherapy rdf:type db:Maastricht.radiotherapyClass. 
 
    ?gender rdf:type db:Maastricht.biological_sex.
    
    ?age rdf:type db:Maastricht.age_at_diagnosis.
    
    ?tumour rdf:type db:Maastricht.index_tumour_location.
    
    ?whostatus rdf:type db:Maastricht.performance_status_ecog.
    
    ?hpv rdf:type db:Maastricht.overall_hpv_p16_status.
    
    ?tstage rdf:type db:Maastricht.clin_t.
    
    ?nstage rdf:type db:Maastricht.clin_n.
    
    ?mstage rdf:type db:Maastricht.clin_m.
    
    ?ajcc rdf:type db:Maastricht.ajcc_stage.
    
    ?asa rdf:type db:Maastricht.pretreat_hb_in_mmolperlitre.
    
    ?surgery rdf:type db:Maastricht.cancer_surgery_performed.
    
    ?chemo rdf:type db:Maastricht.chemotherapy_given.
    
    ?rttotaldays rdf:type db:Maastricht.radiotherapy_total_treat_time.
        
    ?graytotaldose rdf:type db:Maastricht.radiotherapy_refgydose_total_highriskgtv.
        
    ?graydoseperfraction rdf:type db:Maastricht.radiotherapy_refgydose_perfraction_highriskgtv.
    
    ?rtfractions rdf:type db:Maastricht.radiotherapy_number_fractions_highriskgtv.
        
    ?survival rdf:type db:Maastricht.event_overall_survival.
        
    ?overallsurvivaldays rdf:type db:Maastricht.overall_survival_in_days.
    
    ?eventrecurrence rdf:type db:Maastricht.event_recurrence_metastatic_free_survival.
        
    ?eventrecurrencedays rdf:type db:Maastricht.recurrence_metastatic_free_survival_in_days.
        
    ?localrecurrence rdf:type db:Maastricht.event_local_recurrence.
        
    ?localrecurrencedays rdf:type db:Maastricht.local_recurrence_in_days.
    
    ?regionalrecurrence rdf:type db:Maastricht.event_locoregional_recurrence.
    
    ?regionalrecurrencedays rdf:type db:Maastricht.locoregional_recurrence_in_days.
        
    ?metastasis rdf:type db:Maastricht.event_distant_metastases.
        
    ?metastasisdays rdf:type db:Maastricht.distant_metastases_in_days.
        
    }

"""

#query to replace empty cells of HPV column with "Unknown"
queryUnknown = """
PREFIX db: <http://data.local/rdf/ontology/>
PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
PREFIX lidicom: <https://johanvansoest.nl/ontologies/LinkedDicom/>
PREFIX roo: <http://www.cancerdata.org/roo/>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
INSERT  
    {
    
    GRAPH <http://annotations_updated/>
    {
       ?hpvv dbo:has_cell ?hpvcell.
       ?hpvcell dbo:has_value "Unknown".
    }
    }
        WHERE { 
            ?patient roo:P100022 ?hpvv.
            FILTER NOT EXISTS {?hpvv dbo:has_cell ?hpvcell}.
            BIND(IRI(CONCAT(str(?hpvv), "/value")) as ?hpvcell).
    }
    """

#call this function to run a query on your endpoint
def runQuery(endpoint, query):
    annotationResponse = requests.post(endpoint,
                                   data="update=" + query,
                                   headers={
                                       "Content-Type": "application/x-www-form-urlencoded",
                                       # "Accept": "application/json"
                                   })
    output = annotationResponse.text
    print(output)

runQuery(endpoint, queryneoplasm)
runQuery(endpoint, queryclinical)
runQuery(endpoint, queryequiv)
runQuery(endpoint, queryUnknown)

#addmapping function to map the categorical values to its semantical code for clinical data
def addMapping(localTerm, targetClass, superClass):
    queryval = """
            PREFIX db: <http://data.local/rdf/ontology/>
            PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
            PREFIX lidicom: <https://johanvansoest.nl/ontologies/LinkedDicom/>
            PREFIX roo: <http://www.cancerdata.org/roo/>
            PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            INSERT  
                {
                 GRAPH <http://annotations_updated/> {
                    ?term rdf:type owl:Class ;
                     owl:equivalentClass [ owl:intersectionOf 
                                                    ( [ rdf:type owl:Restriction ;
                                                        owl:onProperty dbo:cell_of ;
                                                        owl:someValuesFrom ?superClass;
                                                      ]
                                                      [ rdf:type owl:Restriction ;
                                                        owl:onProperty dbo:has_value ;
                                                        owl:hasValue ?localValue;
                                                      ]
                                                    ) ;
                                 rdf:type owl:Class
                               ] ;
                     rdfs:subClassOf ?superClass .
                }
            } WHERE { 
                BIND(<%s> AS ?term).
                BIND(<%s> AS ?superClass).
                BIND("%s"^^xsd:string AS ?localValue).
            }
            """ % (targetClass, superClass, localTerm)

    annotationResponse = requests.post(endpoint,
                                       data="update=" + queryval,
                                       headers={
                                           "Content-Type": "application/x-www-form-urlencoded"
                                       })
    print(annotationResponse.status_code)


# T stage
addMapping("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48719",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48720",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("2", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48724",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("3", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48728",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping("4", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48732",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")

# N stage
addMapping("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48705",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48706",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping("2", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping("3", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48714",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")

# M stage
addMapping("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48699",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48883")
addMapping("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48700",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48883")

# gender
addMapping("female", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C16576",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28421")
addMapping("male", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C20197",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28421")

# survival
addMapping("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28554",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C25717")
addMapping("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C37987",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C25717")
# 0=alive
# 1=dead

# tumorlocation
addMapping("oropharynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
addMapping("larynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12420",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")

# WHOstatus
addMapping("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105722",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105721")
addMapping("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105723",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105721")

# hpv
addMapping("positive", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C128839",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")
addMapping("negative", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C131488",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")
addMapping("Unknown", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C10000",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")

# ajcc
addMapping("i", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27966",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("ii", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("iii", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27970",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("iva", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("ivb", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping("ivc", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")

# chemo
addMapping("concomitant", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
addMapping("concurrent", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
addMapping("none", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15313",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")

