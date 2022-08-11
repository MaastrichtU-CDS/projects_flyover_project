import requests

endpoint1 = "http://rdf-store:7200/repositories/hn_one/statements"
endpoint2 = "http://rdf-store:7200/repositories/head_neck/statements"
endpoint3 = "http://rdf-store:7200/repositories/opc/statements"
endpoint4 = "http://rdf-store:7200/repositories/hnscc/statements"

query1 = """
PREFIX db: <http://hn_one.local/rdf/ontology/>
PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
PREFIX roo: <http://www.cancerdata.org/roo/>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

INSERT  
    {
    
    GRAPH <http://annotation.local/>
    {
    
     db:hn1_clinical_data_updated_july_2020.years rdf:type owl:Class.  
   
     db:hn1_clinical_data_updated_july_2020.years rdfs:label "Years".
    
     db:hn1_clinical_data_updated_july_2020.days rdf:type owl:Class.
    
     db:hn1_clinical_data_updated_july_2020.days rdfs:label "Days".
    
     db:hn1_clinical_data_updated_july_2020.Gray rdf:type owl:Class. 
  
     db:hn1_clinical_data_updated_july_2020.Gray rdfs:label "Gy".
   
     db:hn1_clinical_data_updated_july_2020.radiotherapyClass rdf:type owl:Class.
    
     db:hn1_clinical_data_updated_july_2020.radiotherapyClass dbo:table db:hn1_clinical_data_updated_july_2020.
    
     db:hn1_clinical_data_updated_july_2020.radiotherapyClass rdfs:label "Radiotherapy".
     
     db:hn1_clinical_data_updated_july_2020.neoplasmClass rdf:type owl:Class. 
     
     db:hn1_clinical_data_updated_july_2020.neoplasmClass dbo:table db:hn1_clinical_data_updated_july_2020.
    
     db:hn1_clinical_data_updated_july_2020.neoplasmClass rdfs:label "Neoplasm".
    
     ?tablerow dbo:has_column ?neoplasm, ?radiotherapy.
    
     ?neoplasm rdf:type db:hn1_clinical_data_updated_july_2020.neoplasmClass.
    
     ?radiotherapy rdf:type db:hn1_clinical_data_updated_july_2020.radiotherapyClass.
  
}
}

where 
{
    BIND(IRI(CONCAT(str(?tablerow), "/neoplasm")) as ?neoplasm).
    
    BIND(IRI(CONCAT(str(?tablerow), "/radiotherapy")) as ?radiotherapy).
    
    ?tablerow rdf:type db:hn1_clinical_data_updated_july_2020.
   
}
        """

query2 = """
PREFIX db: <http://hn_one.local/rdf/ontology/>
PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
PREFIX roo: <http://www.cancerdata.org/roo/>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

INSERT 
{
    GRAPH <http://annotation.local/>
    {
        
	 ?tablerow roo:P100061 ?patientID.   #has_identifier
        
     ?tablerow roo:P100018 ?gender.		 #has_biological_sex
        
     ?tablerow roo:hasage ?age. 

     ?age roo:P100027 db:hn1_clinical_data_updated_july_2020.years.	
        
     ?tablerow roo:P100022 ?hpv.		 #has_finding
        
     ?tablerow roo:P100214 ?asa.		 #has_measurement
        
     ?tablerow roo:haswhostatus ?whostatus.   #has_WHO_status
        
     ?tablerow roo:P100029 ?neoplasm.
   
     ?neoplasm roo:P100244 ?tstage. 	 #has_T_stage
        
     ?neoplasm roo:P100242 ?nstage. 	 #has_N_stage
      
     ?neoplasm roo:P100241 ?mstage. 	 #has_M_stage
            
     ?neoplasm roo:P100219 ?ajcc. 		 #has_AJCC_stage
        
     ?neoplasm roo:P100202 ?tumour.		 #tumourSite
        
     ?neoplasm roo:P10032 ?metastasis. 	 #has_metastasis
        
     ?neoplasm roo:P100022 ?eventrecurrence, ?eventrecurrencedays, ?localrecurrence, ?localrecurrencedays, ?regionalrecurrence, ?regionalrecurrencedays, ?metastasisdays.  #has_finding
        
     ?localrecurrencedays roo:P100027 db:hn1_clinical_data_updated_july_2020.days.
        
     ?regionalrecurrencedays roo:P100027 db:hn1_clinical_data_updated_july_2020.days.
        
     ?metastasisdays roo:P100027 db:hn1_clinical_data_updated_july_2020.days.
        
     ?tablerow roo:P100403 ?radiotherapy. #treated_by 
        
     ?radiotherapy roo:P100027 ?rttotaldays. #has_unit
        
     ?rttotaldays roo:P100027 db:hn1_clinical_data_updated_july_2020.days.
        
     ?radiotherapy roo:P100023 ?graytotaldose. #has_dose
        
     ?graytotaldose roo:P100027 db:hn1_clinical_data_updated_july_2020.Gray.
        
     ?radiotherapy roo:P100214 ?graydoseperfraction.   #has_dose_per_fraction
     
     ?graydoseperfraction roo:P100027 db:hn1_clinical_data_updated_july_2020.Gray.
    
     ?radiotherapy roo:P100224 ?rtfractions. #has_fraction_count
      
     ?tablerow roo:P100403 ?surgery.     #treated_by
     
     ?tablerow roo:P100254 ?survival.    #has_death_finding 
        
     ?tablerow roo:has ?overallsurvivaldays.
        
     ?overallsurvivaldays roo:P100027 db:hn1_clinical_data_updated_july_2020.days.
        
     ?tablerow roo:P100231 ?chemo.        #chemo_administered
      
        
     db:hn1_clinical_data_updated_july_2020 owl:equivalentClass ncit:C16960.
        
     db:hn1_clinical_data_updated_july_2020.id owl:equivalentClass ncit:C25364.
        
     db:hn1_clinical_data_updated_july_2020.biological_sex owl:equivalentClass ncit:C28421.
        
     db:hn1_clinical_data_updated_july_2020.age_at_diagnosis owl:equivalentClass roo:C100003.
    
     db:hn1_clinical_data_updated_july_2020.overall_hpv_p16_status owl:equivalentClass ncit:C14226.
        
     db:hn1_clinical_data_updated_july_2020.pretreat_hb_in_mmolperlitre owl:equivalentClass roo:asaScore.
        
     db:hn1_clinical_data_updated_july_2020.performance_status_ecog owl:equivalentClass ncit:C105721.
        
     db:hn1_clinical_data_updated_july_2020.clin_t owl:equivalentClass ncit:C48885.
     
     db:hn1_clinical_data_updated_july_2020.clin_n owl:equivalentClass ncit:C48884.

	 db:hn1_clinical_data_updated_july_2020.clin_m owl:equivalentClass ncit:C48883.
        
     db:hn1_clinical_data_updated_july_2020.ajcc_stage owl:equivalentClass ncit:C38027.
        
     db:hn1_clinical_data_updated_july_2020.cancer_surgery_performed owl:equivalentClass ncit:C17173.
      
     db:hn1_clinical_data_updated_july_2020.index_tumour_location owl:equivalentClass ncit:C3263.
    
     db:hn1_clinical_data_updated_july_2020.event_recurrence_metastatic_free_survival owl:equivalentClass roo:eventrecurrence.
    
     db:hn1_clinical_data_updated_july_2020.recurrence_metastatic_free_survival_in_days owl:equivalentClass roo:eventrecurrencedays.
                
     db:hn1_clinical_data_updated_july_2020.event_local_recurrence owl:equivalentClass roo:localrecurrence.

	 db:hn1_clinical_data_updated_july_2020.local_recurrence_in_days owl:equivalentClass roo:localrecurrencedays.

	 db:hn1_clinical_data_updated_july_2020.event_locoregional_recurrence owl:equivalentClass roo:regionalrecurrence.

	 db:hn1_clinical_data_updated_july_2020.locoregional_recurrence_in_days owl:equivalentClass roo:regionalrecurrencedays.
        
     db:hn1_clinical_data_updated_july_2020.event_distant_metastases owl:equivalentClass ncit:C19151.
               
     db:hn1_clinical_data_updated_july_2020.distant_metastases_in_days owl:equivalentClass roo:metastasisdays.
        
     db:hn1_clinical_data_updated_july_2020.event_overall_survival owl:equivalentClass ncit:C25717.

	 db:hn1_clinical_data_updated_july_2020.overall_survival_in_days owl:equivalentClass roo:overallsurvivaldays.
        
     db:hn1_clinical_data_updated_july_2020.chemotherapy_given owl:equivalentClass ncit:C15632.
    
     db:hn1_clinical_data_updated_july_2020.radiotherapy_total_treat_time owl:equivalentClass roo:rttotaldays.
    
     db:hn1_clinical_data_updated_july_2020.radiotherapy_refgydose_total_highriskgtv owl:equivalentClass roo:graytotaldose.
        
     db:hn1_clinical_data_updated_july_2020.radiotherapy_refgydose_perfraction_highriskgtv owl:equivalentClass roo:graydoseperfraction.
    
     db:hn1_clinical_data_updated_july_2020.radiotherapy_number_fractions_highriskgtv owl:equivalentClass roo:rttotalfraction.
   
     db:hn1_clinical_data_updated_july_2020.years owl:equivalentClass ncit:C29848.
      
     db:hn1_clinical_data_updated_july_2020.days owl:equivalentClass ncit:C25301. 
    
     db:hn1_clinical_data_updated_july_2020.Gray owl:equivalentClass ncit:C18063.
    
     db:hn1_clinical_data_updated_july_2020.neoplasmClass owl:equivalentClass ncit:C3262.
    
     db:hn1_clinical_data_updated_july_2020.radiotherapyClass owl:equivalentClass ncit:C15313.
    
     dbo:has_value owl:sameAs roo:P100042.    #has_value
    
     dbo:has_unit owl:sameAs roo:P100047.    #has_value
     
     dbo:cell_of rdf:type owl:ObjectProperty;
                 owl:inverseOf dbo:has_cell.
       
    } 
}
  

WHERE

{  
    ?tablerow rdf:type db:hn1_clinical_data_updated_july_2020.
    
	?tablerow dbo:has_column ?patientID, ?gender, ?age, ?tumour, ?whostatus, ?hpv, ?tstage, ?nstage, ?mstage, ?ajcc, ?asa, ?surgery, ?chemo, ?rttotaldays, ?graytotaldose, ?graydoseperfraction, ?survival, ?overallsurvivaldays, ?localrecurrence, ?localrecurrencedays, ?regionalrecurrence, ?regionalrecurrencedays, ?metastasis, ?metastasisdays, ?neoplasm, ?radiotherapy, ?rtfractions, ?eventrecurrence, ?eventrecurrencedays.
          
    ?neoplasm rdf:type db:hn1_clinical_data_updated_july_2020.neoplasmClass.
    
    ?radiotherapy rdf:type db:hn1_clinical_data_updated_july_2020.radiotherapyClass. 
    
    ?patientID rdf:type db:hn1_clinical_data_updated_july_2020.id. 
 
    ?gender rdf:type db:hn1_clinical_data_updated_july_2020.biological_sex.
    
    ?age rdf:type db:hn1_clinical_data_updated_july_2020.age_at_diagnosis.
    
    ?tumour rdf:type db:hn1_clinical_data_updated_july_2020.index_tumour_location.
    
    ?whostatus rdf:type db:hn1_clinical_data_updated_july_2020.performance_status_ecog.
    
    ?hpv rdf:type db:hn1_clinical_data_updated_july_2020.overall_hpv_p16_status.
    
    ?tstage rdf:type db:hn1_clinical_data_updated_july_2020.clin_t.
    
    ?nstage rdf:type db:hn1_clinical_data_updated_july_2020.clin_n.
    
    ?mstage rdf:type db:hn1_clinical_data_updated_july_2020.clin_m.
    
    ?ajcc rdf:type db:hn1_clinical_data_updated_july_2020.ajcc_stage.
    
    ?asa rdf:type db:hn1_clinical_data_updated_july_2020.pretreat_hb_in_mmolperlitre.
    
    ?surgery rdf:type db:hn1_clinical_data_updated_july_2020.cancer_surgery_performed.
    
    ?chemo rdf:type db:hn1_clinical_data_updated_july_2020.chemotherapy_given.
    
    ?rttotaldays rdf:type db:hn1_clinical_data_updated_july_2020.radiotherapy_total_treat_time.
        
    ?graytotaldose rdf:type db:hn1_clinical_data_updated_july_2020.radiotherapy_refgydose_total_highriskgtv.
        
    ?graydoseperfraction rdf:type db:hn1_clinical_data_updated_july_2020.radiotherapy_refgydose_perfraction_highriskgtv.
    
    ?rtfractions rdf:type db:hn1_clinical_data_updated_july_2020.radiotherapy_number_fractions_highriskgtv.
        
    ?survival rdf:type db:hn1_clinical_data_updated_july_2020.event_overall_survival.
        
    ?overallsurvivaldays rdf:type db:hn1_clinical_data_updated_july_2020.overall_survival_in_days.
    
    ?eventrecurrence rdf:type db:hn1_clinical_data_updated_july_2020.event_recurrence_metastatic_free_survival.
        
    ?eventrecurrencedays rdf:type db:hn1_clinical_data_updated_july_2020.recurrence_metastatic_free_survival_in_days.
        
    ?localrecurrence rdf:type db:hn1_clinical_data_updated_july_2020.event_local_recurrence.
        
    ?localrecurrencedays rdf:type db:hn1_clinical_data_updated_july_2020.local_recurrence_in_days.
    
    ?regionalrecurrence rdf:type db:hn1_clinical_data_updated_july_2020.event_locoregional_recurrence.
    
    ?regionalrecurrencedays rdf:type db:hn1_clinical_data_updated_july_2020.locoregional_recurrence_in_days.
        
    ?metastasis rdf:type db:hn1_clinical_data_updated_july_2020.event_distant_metastases.
        
    ?metastasisdays rdf:type db:hn1_clinical_data_updated_july_2020.distant_metastases_in_days.
 
}

"""
def runQuery(endpoint, query):
    annotationResponse = requests.post(endpoint,
                                   data="update=" + query,
                                   headers={
                                       "Content-Type": "application/x-www-form-urlencoded",
                                       # "Accept": "application/json"
                                   })
    output = annotationResponse.text
    print(output)

runQuery(endpoint1, query1)
runQuery(endpoint1, query2)

def addMapping1(localTerm, targetClass, superClass):
    query3 = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX db: <http://hn_one.local/rdf/ontology/>
            PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
            INSERT {
                GRAPH <http://annotation.local/> {
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

    annotationResponse = requests.post(endpoint1,
                                       data="update=" + query3,
                                       headers={
                                           "Content-Type": "application/x-www-form-urlencoded"
                                       })
    print(annotationResponse.status_code)


# T stage
addMapping1("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48719",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping1("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48720",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping1("2", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48724",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping1("3", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48728",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping1("4", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48732",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")

# N stage
addMapping1("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48705",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping1("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48706",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping1("2", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping1("3", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48714",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")

# M stage
addMapping1("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48699",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48883")
addMapping1("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48700",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48883")

# gender
addMapping1("female", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C16576",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28421")
addMapping1("male", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C20197",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28421")

# survival
addMapping1("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28554",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C25717")
addMapping1("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C37987",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C25717")
# 0=alive
# 1=dead

# tumorlocation
addMapping1("oropharynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
addMapping1("larynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12420",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")

# WHOstatus
addMapping1("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105722",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105721")
addMapping1("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105723",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105721")

# hpv
addMapping1("positive", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C128839",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")
addMapping1("negative", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C131488",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")

# ajcc
addMapping1("i", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27966",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping1("ii", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping1("iii", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27970",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping1("iva", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping1("ivb", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping1("ivc", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")

# chemo
addMapping1("concomitant", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
addMapping1("none", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15313",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")

query4 = """
PREFIX db: <http://head_neck.local/rdf/ontology/>
PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
PREFIX roo: <http://www.cancerdata.org/roo/>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

INSERT  
    {
    GRAPH <http://annotation.local/>
    {
    
     db:infoclinical_hn_version2_30may2018_concat.years rdf:type owl:Class.  
   
     db:infoclinical_hn_version2_30may2018_concat.years rdfs:label "Years".
    
     db:infoclinical_hn_version2_30may2018_concat.days rdf:type owl:Class.
    
     db:infoclinical_hn_version2_30may2018_concat.days rdfs:label "Days".
    
     db:infoclinical_hn_version2_30may2018_concat.Gray rdf:type owl:Class. 
  
     db:infoclinical_hn_version2_30may2018_concat.Gray rdfs:label "Gy".
   
     db:infoclinical_hn_version2_30may2018_concat.radiotherapyClass rdf:type owl:Class.
    
     db:infoclinical_hn_version2_30may2018_concat.radiotherapyClass dbo:table db:infoclinical_hn_version2_30may2018_concat.
    
     db:infoclinical_hn_version2_30may2018_concat.radiotherapyClass rdfs:label "Radiotherapy".
     
     db:infoclinical_hn_version2_30may2018_concat.neoplasmClass rdf:type owl:Class. 
     
     db:infoclinical_hn_version2_30may2018_concat.neoplasmClass dbo:table db:infoclinical_hn_version2_30may2018_concat.
     
     db:infoclinical_hn_version2_30may2018_concat.neoplasmClass rdfs:label "Neoplasm".
    
     ?tablerowMon dbo:has_column ?neoplasmMon, ?radiotherapyMon.
     
     ?neoplasmMon rdf:type db:infoclinical_hn_version2_30may2018_concat.neoplasmClass.
    
     ?radiotherapyMon rdf:type db:infoclinical_hn_version2_30may2018_concat.radiotherapyClass.
    } 
}

where 
{
    BIND(IRI(CONCAT(str(?tablerowMon), "/neoplasm")) as ?neoplasmMon).
    
    BIND(IRI(CONCAT(str(?tablerowMon), "/radiotherapy")) as ?radiotherapyMon).
    
    ?tablerowMon rdf:type db:infoclinical_hn_version2_30may2018_concat.
   
}
        """

query5 = """
PREFIX db: <http://head_neck.local/rdf/ontology/>
PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
PREFIX roo: <http://www.cancerdata.org/roo/>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

INSERT 
{
    GRAPH <http://annotation.local/>
    {
        
     ?tablerowMon roo:P100061 ?patientIDMon.   #has_identifier
        
     ?tablerowMon roo:P100018 ?genderMon.        #has_biological_sex
        
     ?tablerowMon roo:hasage ?ageMon. 
    
     ?ageMon roo:P100027 db:infoclinical_hn_version2_30may2018_concat.years.    
        
     ?tablerowMon roo:P100022 ?hpvMon.       #has_finding
   
     ?tablerowMon roo:P100229 ?followupMon.
        
     ?tablerowMon roo:P100029 ?neoplasmMon.
   
     ?neoplasmMon roo:P100244 ?tstageMon.    #has_T_stage
        
     ?neoplasmMon roo:P100242 ?nstageMon.    #has_N_stage
      
     ?neoplasmMon roo:P100241 ?mstageMon.    #has_M_stage
        
     ?neoplasmMon roo:P100219 ?ajccMon.
    
     ?neoplasmMon roo:P100202 ?tumourMon.        #tumourSite
        
     ?neoplasmMon roo:P10032 ?metastasisMon.     #has_metastasis
        
     ?neoplasmMon roo:P100022 ?regionalrecurrenceMon, ?regionalrecurrencedaysMon, ?metastasisdaysMon.  #has_finding
    
     ?regionalrecurrencedaysMon roo:P100027 db:infoclinical_hn_version2_30may2018_concat.days.
        
     ?metastasisdaysMon roo:P100027 db:infoclinical_hn_version2_30may2018_concat.days.
        
     ?tablerowMon roo:P100403 ?radiotherapyMon. #treated_by 
    
     ?tablerowMon roo:P100403 ?surgeryMon.     #treated_by
     
     ?tablerowMon roo:P100254 ?survivalMon.    #has_death_finding 
        
     ?tablerowMon roo:has ?overallsurvivaldaysMon.
        
     ?overallsurvivaldaysMon roo:P100027 db:infoclinical_hn_version2_30may2018_concat.days.
        
     ?tablerowMon roo:P100231 ?chemoMon. 
    
    
     db:infoclinical_hn_version2_30may2018_concat owl:equivalentClass ncit:C16960.
        
     db:infoclinical_hn_version2_30may2018_concat.patient owl:equivalentClass ncit:C25364.
        
     db:infoclinical_hn_version2_30may2018_concat.sex owl:equivalentClass ncit:C28421.
        
     db:infoclinical_hn_version2_30may2018_concat.age owl:equivalentClass roo:C100003.
    
     db:infoclinical_hn_version2_30may2018_concat.hpv_status owl:equivalentClass ncit:C14226.
    
     db:infoclinical_hn_version2_30may2018_concat.time_diagnosis_to_last_follow_up_days owl:equivalentClass roo:followupdays.
        
     db:infoclinical_hn_version2_30may2018_concat.t_stage owl:equivalentClass ncit:C48885.
     
     db:infoclinical_hn_version2_30may2018_concat.n_stage owl:equivalentClass ncit:C48884.

     db:infoclinical_hn_version2_30may2018_concat.m_stage owl:equivalentClass ncit:C48883.
        
     db:infoclinical_hn_version2_30may2018_concat.tnm_group_stage owl:equivalentClass ncit:C38027.
    
     db:infoclinical_hn_version2_30may2018_concat.surgery owl:equivalentClass ncit:C17173.
      
     db:infoclinical_hn_version2_30may2018_concat.primary_site owl:equivalentClass ncit:C3263.
    
     db:infoclinical_hn_version2_30may2018_concat.locoregional owl:equivalentClass roo:regionalrecurrence.

     db:infoclinical_hn_version2_30may2018_concat.time_diagnosis_to_lr_days owl:equivalentClass roo:regionalrecurrencedays.
        
     db:infoclinical_hn_version2_30may2018_concat.distant owl:equivalentClass ncit:C19151.
               
     db:infoclinical_hn_version2_30may2018_concat.time_diagnosis_to_dm_days owl:equivalentClass roo:metastasisdays.
        
     db:infoclinical_hn_version2_30may2018_concat.death owl:equivalentClass ncit:C25717.

     db:infoclinical_hn_version2_30may2018_concat.time_diagnosis_to_death_days owl:equivalentClass roo:overallsurvivaldays.
        
     db:infoclinical_hn_version2_30may2018_concat.therapy owl:equivalentClass ncit:C15632.

     db:infoclinical_hn_version2_30may2018_concat.years owl:equivalentClass ncit:C29848.
      
     db:infoclinical_hn_version2_30may2018_concat.days owl:equivalentClass ncit:C25301. 
    
     db:infoclinical_hn_version2_30may2018_concat.Gray owl:equivalentClass ncit:C18063.
    
     db:infoclinical_hn_version2_30may2018_concat.neoplasmClass owl:equivalentClass ncit:C3262.
    
     db:infoclinical_hn_version2_30may2018_concat.radiotherapyClass owl:equivalentClass ncit:C15313.
    
     dbo:has_value owl:sameAs roo:P100042.    #has_value
    
     dbo:has_unit owl:sameAs roo:P100047.    #has_value
     
     dbo:cell_of rdf:type owl:ObjectProperty;
                 owl:inverseOf dbo:has_cell.
       
    } 
}  

WHERE

{  
    ?tablerowMon rdf:type db:infoclinical_hn_version2_30may2018_concat.
    
    ?tablerowMon dbo:has_column ?patientIDMon, ?genderMon, ?ageMon, ?tumourMon, ?hpvMon, ?tstageMon, ?nstageMon, ?mstageMon, ?surgeryMon, ?survivalMon, ?overallsurvivaldaysMon, ?regionalrecurrenceMon, ?regionalrecurrencedaysMon, ?metastasisMon, ?metastasisdaysMon, ?followupMon, ?neoplasmMon, ?radiotherapyMon, ?ajccMon, ?chemoMon.
          
    ?neoplasmMon rdf:type db:infoclinical_hn_version2_30may2018_concat.neoplasmClass.
    
    ?radiotherapyMon rdf:type db:infoclinical_hn_version2_30may2018_concat.radiotherapyClass. 
    
    ?patientIDMon rdf:type db:infoclinical_hn_version2_30may2018_concat.patient. 
 
    ?genderMon rdf:type db:infoclinical_hn_version2_30may2018_concat.sex.
    
    ?ageMon rdf:type db:infoclinical_hn_version2_30may2018_concat.age.
    
    ?tumourMon rdf:type db:infoclinical_hn_version2_30may2018_concat.primary_site.
    
    ?hpvMon rdf:type db:infoclinical_hn_version2_30may2018_concat.hpv_status.
    
    ?followupMon rdf:type db:infoclinical_hn_version2_30may2018_concat.time_diagnosis_to_last_follow_up_days.
    
    ?tstageMon rdf:type db:infoclinical_hn_version2_30may2018_concat.t_stage.
    
    ?nstageMon rdf:type db:infoclinical_hn_version2_30may2018_concat.n_stage.
    
    ?mstageMon rdf:type db:infoclinical_hn_version2_30may2018_concat.m_stage.
    
    ?ajccMon rdf:type db:infoclinical_hn_version2_30may2018_concat.tnm_group_stage.
  
    ?surgeryMon rdf:type db:infoclinical_hn_version2_30may2018_concat.surgery.
    
    ?chemoMon rdf:type db:infoclinical_hn_version2_30may2018_concat.therapy.
 
    ?survivalMon rdf:type db:infoclinical_hn_version2_30may2018_concat.death.
        
    ?overallsurvivaldaysMon rdf:type db:infoclinical_hn_version2_30may2018_concat.time_diagnosis_to_death_days.
  
    ?regionalrecurrenceMon rdf:type db:infoclinical_hn_version2_30may2018_concat.locoregional.
    
    ?regionalrecurrencedaysMon rdf:type db:infoclinical_hn_version2_30may2018_concat.time_diagnosis_to_lr_days.
        
    ?metastasisMon rdf:type db:infoclinical_hn_version2_30may2018_concat.distant.
        
    ?metastasisdaysMon rdf:type db:infoclinical_hn_version2_30may2018_concat.time_diagnosis_to_dm_days.
 
}

"""
runQuery(endpoint2, query4)
runQuery(endpoint2, query5)

def addMapping2(localTerm, targetClass, superClass):
    query6 = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX db: <http://head_neck.local/rdf/ontology/>
            PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
            INSERT {
                GRAPH <http://annotation.local/> {
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

    annotationResponse = requests.post(endpoint2,
                                       data="update=" + query6,
                                       headers={
                                           "Content-Type": "application/x-www-form-urlencoded"
                                       })
    print(annotationResponse.status_code)

# T stage
addMapping2("Tx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48737",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping2("T1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48720",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping2("T2", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48724",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping2("T3", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48728",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping2("T4", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48732",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")

# N stage
addMapping2("N0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48705",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping2("N1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48706",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping2("N2", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping2("N3", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48714",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")

# M stage
addMapping2("M0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48699",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48883")
addMapping2("M1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48700",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48883")

# gender
addMapping2("F", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C16576",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28421")
addMapping2("M", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C20197",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28421")

# survival
addMapping2("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28554",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C25717")
addMapping2("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C37987",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C25717")

# tumorlocation
addMapping2("Oropharynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
addMapping2("Larynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12420",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
addMapping2("Hypopharynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12246",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
addMapping2("Nasopharynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12423",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")

# hpv
addMapping2("%2B", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C128839",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")
addMapping2("-", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C131488",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")

# ajcc
addMapping2("stage I", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27966",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping2("Stade I", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27966",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping2("stage I", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27966",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")

addMapping2("Stade II", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping2("stage II", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping2("StageII", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping2("Stage II", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping2("stage IIB", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping2("Stage IIB", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")

addMapping2("stage III", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27970",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping2("Stade III", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27970",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping2("Stage III", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27970",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")

addMapping2("Stage IV", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping2("stage IV", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")

addMapping2("Stade IVA", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping2("Stage IVA", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping2("stage IVA", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping2("stage IVB", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping2("Stade IVB", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")

# chemo
addMapping2("chemo radiation", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
addMapping2("radiation", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15313",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")

query7 = """
PREFIX db: <http://opc.local/rdf/ontology/>
PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
PREFIX roo: <http://www.cancerdata.org/roo/>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
INSERT    
    {
     GRAPH <http://annotation.local/>
    {
    
     db:clinical_data_list_opc_v3.years rdf:type owl:Class.  
   
     db:clinical_data_list_opc_v3.years rdfs:label "Years".
    
     db:clinical_data_list_opc_v3.days rdf:type owl:Class.
    
     db:clinical_data_list_opc_v3.days rdfs:label "Days".
    
     db:clinical_data_list_opc_v3.Gray rdf:type owl:Class. 
  
     db:clinical_data_list_opc_v3.Gray rdfs:label "Gy".
   
     db:clinical_data_list_opc_v3.radiotherapyClass rdf:type owl:Class.
    
     db:clinical_data_list_opc_v3.radiotherapyClass dbo:table db:clinical_data_list_opc_v3.
   
     db:clinical_data_list_opc_v3.radiotherapyClass rdfs:label "Radiotherapy".
     
     db:clinical_data_list_opc_v3.neoplasmClass rdf:type owl:Class. 
     
     db:clinical_data_list_opc_v3.neoplasmClass dbo:table db:clinical_data_list_opc_v3.

     db:clinical_data_list_opc_v3.neoplasmClass rdfs:label "Neoplasm".
    
     ?tablerowTor dbo:has_column ?neoplasmTor, ?radiotherapyTor.
     
     ?neoplasmTor rdf:type db:clinical_data_list_opc_v3.neoplasmClass.
    
     ?radiotherapyTor rdf:type db:clinical_data_list_opc_v3.radiotherapyClass.
        
    }
}

where 
{
    BIND(IRI(CONCAT(str(?tablerowTor), "/neoplasm")) as ?neoplasmTor).
    
    BIND(IRI(CONCAT(str(?tablerowTor), "/radiotherapy")) as ?radiotherapyTor).
    
    ?tablerowTor rdf:type db:clinical_data_list_opc_v3.
   
}
        """

query8 = """
PREFIX db: <http://opc.local/rdf/ontology/>
PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
PREFIX roo: <http://www.cancerdata.org/roo/>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

INSERT 
{
     GRAPH <http://annotation.local/>
    {
        
     ?tablerowTor roo:P100061 ?patientIDTor.   #has_identifier
        
     ?tablerowTor roo:P100018 ?genderTor.        #has_biological_sex
        
     ?tablerowTor roo:hasage ?ageTor.  
    
     ?ageTor roo:P100027 db:clinical_data_list_opc_v3.years.    
        
     ?tablerowTor roo:P100022 ?hpvTor.       #has_finding
     
     ?tablerowTor roo:has_smoking_status ?smokingTor.
    
     ?tablerowTor roo:P100229 ?followupdays.
    
     ?followupdays roo:P100027 db:clinical_data_list_opc_v3.days.
 
     ?tablerowTor roo:haswhostatus ?whostatusTor.   #has_WHO_status
        
     ?tablerowTor roo:P100029 ?neoplasmTor.
   
     ?neoplasmTor roo:P100244 ?tstageTor.    #has_T_stage
        
     ?neoplasmTor roo:P100242 ?nstageTor.    #has_N_stage
      
     ?neoplasmTor roo:P100241 ?mstageTor.    #has_M_stage
        
     ?neoplasmTor roo:P100219 ?ajccTor.
           
     ?neoplasmTor roo:P100202 ?tumourTor.        #tumourSite
    
     ?neoplasmTor roo:P10032 ?metastasisTor.     #has_metastasis
        
     ?neoplasmTor roo:P100022 ?localrecurrenceTor, ?localrecurrencedaysTor, ?regionalrecurrenceTor, ?regionalrecurrencedaysTor, ?metastasisdaysTor.  #has_finding
        
     ?localrecurrencedaysTor roo:P100027 db:clinical_data_list_opc_v3.days.
        
     ?regionalrecurrencedaysTor roo:P100027 db:clinical_data_list_opc_v3.days.
        
     ?metastasisdaysTor roo:P100027 db:clinical_data_list_opc_v3.days.
   
     ?tablerowTor roo:P100403 ?radiotherapyTor. #treated_by
        
     ?radiotherapyTor roo:P100027 ?rttotaldaysTor. 
        
     ?rttotaldaysTor roo:P100027 db:clinical_data_list_opc_v3.days.
        
     ?radiotherapyTor roo:P100023 ?graytotaldoseTor. #has_dose
     
     ?radiotherapyTor roo:P100224 ?rtfractionsTor. #has_fraction_count
        
     ?graytotaldoseTor roo:P100027 db:clinical_data_list_opc_v3.Gray.
  
     ?tablerowTor roo:P100231 ?chemoTor.        #chemo_administered
    
     ?tablerowTor roo:P100254 ?survivalTor.    #has_death_finding
      
        
     db:clinical_data_list_opc_v3 owl:equivalentClass ncit:C16960.
        
     db:clinical_data_list_opc_v3.trial_patientid owl:equivalentClass ncit:C25364.
        
     db:clinical_data_list_opc_v3.sex owl:equivalentClass ncit:C28421.
        
     db:clinical_data_list_opc_v3.age_at_diagnosis owl:equivalentClass roo:C100003.
    
     db:clinical_data_list_opc_v3.hpv_p16_status_ihc owl:equivalentClass ncit:C14226.
        
     db:clinical_data_list_opc_v3.ecog_performance_status_scale owl:equivalentClass ncit:C105721.
        
     db:clinical_data_list_opc_v3.t owl:equivalentClass ncit:C48885.
     
     db:clinical_data_list_opc_v3.n owl:equivalentClass ncit:C48884.

     db:clinical_data_list_opc_v3.m owl:equivalentClass ncit:C48883.
        
     db:clinical_data_list_opc_v3.stage_ajcc_7th_edition owl:equivalentClass ncit:C38027.
     
     db:clinical_data_list_opc_v3.smoking_hx owl:equivalentClass ncit:C156825.
        
     db:clinical_data_list_opc_v3.ds_site owl:equivalentClass ncit:C3263.
   
     db:clinical_data_list_opc_v3.interval_from_the_date_of_diagnosis_to_the_date_of_last_fu_days owl:equivalentClass roo:followupdays.
        
     db:clinical_data_list_opc_v3.chemotherapy owl:equivalentClass ncit:C15632.
    
     db:clinical_data_list_opc_v3.time_interval_from_the_date_of_diagnosis_to_the_rt_end_date_day owl:equivalentClass roo:rttotaldays.
    
     db:clinical_data_list_opc_v3.dose_gy owl:equivalentClass roo:graytotaldose.
     
     db:clinical_data_list_opc_v3.number_of_fractions owl:equivalentClass roo:rttotalfraction.
 
     db:clinical_data_list_opc_v3.status owl:equivalentClass ncit:C25717.
    
     db:clinical_data_list_opc_v3.local_failure owl:equivalentClass roo:localrecurrence.
    
     db:clinical_data_list_opc_v3.from_the_date_of_diagnosis_to_the_date_of_local_failure_days owl:equivalentClass roo:localrecurrencedays.

     db:clinical_data_list_opc_v3.regional_failure owl:equivalentClass roo:regionalrecurrence.

     db:clinical_data_list_opc_v3.from_the_date_of_diagnosis_to_the_date_of_regional_failure_days owl:equivalentClass roo:regionalrecurrencedays.
        
     db:clinical_data_list_opc_v3.distant_failure owl:equivalentClass ncit:C19151.
     
     db:clinical_data_list_opc_v3.from_the_date_of_diagnosis_to_the_date_of_distant_failure_days owl:equivalentClass roo:metastasisdays.
   
     db:clinical_data_list_opc_v3.years owl:equivalentClass ncit:C29848.
      
     db:clinical_data_list_opc_v3.days owl:equivalentClass ncit:C25301. 
    
     db:clinical_data_list_opc_v3.Gray owl:equivalentClass ncit:C18063.
    
     db:clinical_data_list_opc_v3.neoplasmClass owl:equivalentClass ncit:C3262.
    
     db:clinical_data_list_opc_v3.radiotherapyClass owl:equivalentClass ncit:C15313.
    
     dbo:has_value owl:sameAs roo:P100042.    #has_value
    
     dbo:has_unit owl:sameAs roo:P100047.    #has_value
     
     dbo:cell_of rdf:type owl:ObjectProperty;
                 owl:inverseOf dbo:has_cell.
       
    } 
}
  
WHERE

{  
    ?tablerowTor rdf:type db:clinical_data_list_opc_v3.
    
    ?tablerowTor dbo:has_column ?patientIDTor, ?genderTor, ?ageTor, ?hpvTor, ?whostatusTor, ?smokingTor, ?tstageTor, ?nstageTor, ?mstageTor, ?tumourTor, ?rttotaldaysTor, ?graytotaldoseTor, ?rtfractionsTor, ?chemoTor, ?followupdays, ?neoplasmTor, ?radiotherapyTor, ?survivalTor, ?metastasisTor, ?localrecurrenceTor, ?localrecurrencedaysTor, ?regionalrecurrenceTor, ?regionalrecurrencedaysTor, ?metastasisdaysTor, ?ajccTor.
          
    ?neoplasmTor rdf:type db:clinical_data_list_opc_v3.neoplasmClass.
    
    ?radiotherapyTor rdf:type db:clinical_data_list_opc_v3.radiotherapyClass. 
    
    ?patientIDTor rdf:type db:clinical_data_list_opc_v3.trial_patientid. 
 
    ?genderTor rdf:type db:clinical_data_list_opc_v3.sex.
    
    ?ageTor rdf:type db:clinical_data_list_opc_v3.age_at_diagnosis.
    
    ?tumourTor rdf:type db:clinical_data_list_opc_v3.ds_site.
    
    ?whostatusTor rdf:type db:clinical_data_list_opc_v3.ecog_performance_status_scale.
    
    ?smokingTor rdf:type db:clinical_data_list_opc_v3.smoking_hx.
    
    ?hpvTor rdf:type db:clinical_data_list_opc_v3.hpv_p16_status_ihc.
    
    ?tstageTor rdf:type db:clinical_data_list_opc_v3.t.
    
    ?nstageTor rdf:type db:clinical_data_list_opc_v3.n.
    
    ?mstageTor rdf:type db:clinical_data_list_opc_v3.m.
    
    ?ajccTor rdf:type db:clinical_data_list_opc_v3.stage_ajcc_7th_edition.
    
    ?chemoTor rdf:type db:clinical_data_list_opc_v3.chemotherapy.
    
    ?rttotaldaysTor rdf:type db:clinical_data_list_opc_v3.time_interval_from_the_date_of_diagnosis_to_the_rt_end_date_day.
        
    ?graytotaldoseTor rdf:type db:clinical_data_list_opc_v3.dose_gy.
        
    ?rtfractionsTor rdf:type db:clinical_data_list_opc_v3.number_of_fractions.
        
    ?followupdays rdf:type db:clinical_data_list_opc_v3.interval_from_the_date_of_diagnosis_to_the_date_of_last_fu_days.
    
    ?survivalTor rdf:type db:clinical_data_list_opc_v3.status.
    
    ?localrecurrenceTor rdf:type db:clinical_data_list_opc_v3.local_failure.
        
    ?localrecurrencedaysTor rdf:type db:clinical_data_list_opc_v3.from_the_date_of_diagnosis_to_the_date_of_local_failure_days.
    
    ?regionalrecurrenceTor rdf:type db:clinical_data_list_opc_v3.regional_failure.
    
    ?regionalrecurrencedaysTor rdf:type db:clinical_data_list_opc_v3.from_the_date_of_diagnosis_to_the_date_of_regional_failure_days.
        
    ?metastasisTor rdf:type db:clinical_data_list_opc_v3.distant_failure.
        
    ?metastasisdaysTor rdf:type db:clinical_data_list_opc_v3.from_the_date_of_diagnosis_to_the_date_of_distant_failure_days.
   
}
"""
runQuery(endpoint3, query7)
runQuery(endpoint3, query8)

def addMapping3(localTerm, targetClass, superClass):
    query9 = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX db: <http://opc.local/rdf/ontology/>
            PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
            INSERT {
                GRAPH <http://annotation.local/> {
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

    annotationResponse = requests.post(endpoint3,
                                       data="update=" + query9,
                                       headers={
                                           "Content-Type": "application/x-www-form-urlencoded"
                                       })
    print(annotationResponse.status_code)


# T stage
addMapping3("T0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48719",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping3("T1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48720",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping3("T2", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48724",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping3("T3", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48728",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping3("T4a", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48732",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping3("T4b", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48732",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")

# N stage
addMapping3("N0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48705",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping3("N1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48706",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping3("N2a", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping3("N2b", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping3("N2c", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping3("N3", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48714",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")

# M stage
addMapping3("M0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48699",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48883")
addMapping3("M1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48700",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48883")

# gender
addMapping3("Female", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C16576",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28421")
addMapping3("Male", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C20197",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28421")

# survival
addMapping3("Dead", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28554",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C25717")
addMapping3("Alive", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C37987",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C25717")
# 0=alive
# 1=dead

# tumorlocation
addMapping3("Oropharynx", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")

# WHOstatus
addMapping3("ECOG 0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105722",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105721")
addMapping3("ECOG 1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105723",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C105721")

#hpv
addMapping3("  positive", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C128839", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")
addMapping3("Positive", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C128839", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")
addMapping3("Positive -Strong", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C128839", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")
addMapping3("Positive -focal", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C128839", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")
addMapping3("Negative", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C131488", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")
addMapping3("  Negative", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C131488", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")


# ajcc
addMapping3("I", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27966",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping3("II", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping3("III", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27970",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping3("IVA", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping3("IVB", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")

# chemo
addMapping3("Yes", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
addMapping3("none", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15313",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")

query10 = """
PREFIX db: <http://hnscc.local/rdf/ontology/>
PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
PREFIX roo: <http://www.cancerdata.org/roo/>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

INSERT   
    {
     GRAPH <http://annotation.local/>
    {    
     db:hnscc_clinical_data.years rdf:type owl:Class.  
   
     db:hnscc_clinical_data.years rdfs:label "Years".
    
     db:hnscc_clinical_data.days rdf:type owl:Class.
    
     db:hnscc_clinical_data.days rdfs:label "Days".
    
     db:hnscc_clinical_data.Gray rdf:type owl:Class. 
  
     db:hnscc_clinical_data.Gray rdfs:label "Gy".
   
     db:hnscc_clinical_data.radiotherapyClass rdf:type owl:Class.
    
     db:hnscc_clinical_data.radiotherapyClass dbo:table db:hnscc_clinical_data.
    
     db:hnscc_clinical_data.radiotherapyClass rdfs:label "Radiotherapy".
     
     db:hnscc_clinical_data.neoplasmClass rdf:type owl:Class. 
     
     db:hnscc_clinical_data.neoplasmClass dbo:table db:hnscc_clinical_data.
        
     db:hnscc_clinical_data.neoplasmClass rdfs:label "Neoplasm".
    
     ?tablerowHous dbo:has_column ?neoplasmHous, ?radiotherapyHous.
     
     ?neoplasmHous rdf:type db:hnscc_clinical_data.neoplasmClass.
    
     ?radiotherapyHous rdf:type db:hnscc_clinical_data.radiotherapyClass.
        
    } 
}
where 
{
    BIND(IRI(CONCAT(str(?tablerowHous), "/neoplasm")) as ?neoplasmHous).
    
    BIND(IRI(CONCAT(str(?tablerowHous), "/radiotherapy")) as ?radiotherapyHous).
    
    ?tablerowHous rdf:type db:hnscc_clinical_data.
   
}
        """

query11 = """
PREFIX db: <http://hnscc.local/rdf/ontology/>
PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
PREFIX roo: <http://www.cancerdata.org/roo/>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

INSERT 
{
     GRAPH <http://annotation.local/>
    {      
     ?tablerowHous roo:P100061 ?patientIDHous.   #has_identifier
     
     ?tablerowHous roo:hasage ?ageHous.  
    
     ?ageHous roo:P100027 db:hnscc_clinical_data.years. 
 
     ?tablerowHous roo:P100018 ?genderHous.
    
     ?tablerowHous roo:P100022 ?hpvHous.
    
     ?tablerowHous roo:P100029 ?neoplasmHous.
     
     ?neoplasmHous roo:P100219 ?ajccHous.
    
     ?neoplasmHous roo:P100244 ?tstageHous.     
        
     ?neoplasmHous roo:P100242 ?nstageHous. 
        
     ?neoplasmHous roo:P100202 ?tumourHous.
    
     ?neoplasmHous roo:P10032 ?metastasisHous.   
    
     ?neoplasmHous roo:P100022 ?localrecurrenceHous, ?localrecurrencedaysHous, ?regionalrecurrenceHous, ?regionalrecurrencedaysHous, ?metastasisdaysHous. 
        
     ?localrecurrencedaysHous roo:P100027 db:hnscc_clinical_data.days.
        
     ?regionalrecurrencedaysHous roo:P100027 db:hnscc_clinical_data.days.
        
     ?metastasisdaysHous roo:P100027 db:hnscc_clinical_data.days.
        
     ?tablerowHous roo:P100403 ?radiotherapyHous. 
        
     ?radiotherapyHous roo:P100027 ?rttotaldaysHous. 
        
     ?rttotaldaysHous roo:P100027 db:hnscc_clinical_data.days.
        
     ?radiotherapyHous roo:P100023 ?graytotaldoseHous.
        
     ?graytotaldoseHous roo:P100027 db:hnscc_clinical_data.Gray.
        
     ?radiotherapyHous roo:P100214 ?graydoseperfractionHous.
     
     ?graydoseperfractionHous roo:P100027 db:hnscc_clinical_data.Gray.
    
     ?radiotherapyHous roo:P100224 ?rtfractionsHous.
    
     ?tablerowHous roo:P100254 ?survivalHous.
        
     ?tablerowHous roo:has ?overallsurvivaldaysHous.
    
     ?tablerowHous roo:P100229 ?followupHous.
    
     ?followupHous roo:P100027 db:hnscc_clinical_data.days.
        
     ?tablerowHous roo:P100231 ?chemoHous.
       
    
     db:hnscc_clinical_data owl:equivalentClass ncit:C16960.
        
     db:hnscc_clinical_data.tcia_radiomics_id owl:equivalentClass ncit:C25364.
            
     db:hnscc_clinical_data.age_at_diag owl:equivalentClass roo:C100003.
    
     db:hnscc_clinical_data.gender owl:equivalentClass ncit:C28421.
    
     db:hnscc_clinical_data.hpv_status owl:equivalentClass ncit:C14226.
    
     db:hnscc_clinical_data.ajcc_stage_7th_edition owl:equivalentClass ncit:C38027.
    
     db:hnscc_clinical_data.cancer_subsite_of_origin owl:equivalentClass ncit:C3263.
    
     db:hnscc_clinical_data.t_category owl:equivalentClass ncit:C48885.
     
     db:hnscc_clinical_data.n_category owl:equivalentClass ncit:C48884.
    
     db:hnscc_clinical_data.radiation_treatment_duration owl:equivalentClass roo:rttotaldays.
    
     db:hnscc_clinical_data.total_prescribed_radiation_treatment_dose owl:equivalentClass roo:graytotaldose.
        
     db:hnscc_clinical_data.radiation_treatment_dose_per_fraction owl:equivalentClass roo:graydoseperfraction.
    
     db:hnscc_clinical_data.radiation_treatment_number_of_fractions owl:equivalentClass roo:rttotalfraction.
    
     db:hnscc_clinical_data.vital_status owl:equivalentClass ncit:C25717.

     db:hnscc_clinical_data.overall_survival_duration owl:equivalentClass roo:overallsurvivaldays.
    
     db:hnscc_clinical_data.local_control owl:equivalentClass roo:localrecurrence.

     db:hnscc_clinical_data.local_control_duration owl:equivalentClass roo:localrecurrencedays.

     db:hnscc_clinical_data.regional_control owl:equivalentClass roo:regionalrecurrence.

     db:hnscc_clinical_data.regional_control_duration owl:equivalentClass roo:regionalrecurrencedays.
        
     db:hnscc_clinical_data.freedom_from_distant_metastasis owl:equivalentClass ncit:C19151.
               
     db:hnscc_clinical_data.freedom_from_distant_metastasis_duration owl:equivalentClass roo:metastasisdays.
    
     db:hnscc_clinical_data.days_to_last_fu owl:equivalentClass roo:followupdays.
        
     db:hnscc_clinical_data.therapeutic_combination owl:equivalentClass ncit:C15632.
    
     db:hnscc_clinical_data.years owl:equivalentClass ncit:C29848.
      
     db:hnscc_clinical_data.days owl:equivalentClass ncit:C25301. 
    
     db:hnscc_clinical_data.Gray owl:equivalentClass ncit:C18063.
    
     db:hnscc_clinical_data.neoplasmClass owl:equivalentClass ncit:C3262.
    
     db:hnscc_clinical_data.radiotherapyClass owl:equivalentClass ncit:C15313.
    
     dbo:has_value owl:sameAs roo:P100042.    #has_value
    
     dbo:has_unit owl:sameAs roo:P100047.    #has_value
     
     dbo:cell_of rdf:type owl:ObjectProperty;
                 owl:inverseOf dbo:has_cell.
       
    } 
}
WHERE
{  
    ?tablerowHous rdf:type db:hnscc_clinical_data.
    
    ?tablerowHous dbo:has_column ?patientIDHous, ?ageHous, ?genderHous, ?hpvHous, ?ajccHous, ?tumourHous, ?neoplasmHous, ?radiotherapyHous, ?tstageHous, ?nstageHous, ?rttotaldaysHous, ?graytotaldoseHous, ?graydoseperfractionHous, ?rtfractionsHous, ?survivalHous, ?overallsurvivaldaysHous, ?metastasisHous, ?localrecurrenceHous, ?localrecurrencedaysHous, ?regionalrecurrenceHous, ?regionalrecurrencedaysHous, ?metastasisdaysHous, ?followupHous, ?chemoHous.
    
    ?neoplasmHous rdf:type db:hnscc_clinical_data.neoplasmClass.
    
    ?radiotherapyHous rdf:type db:hnscc_clinical_data.radiotherapyClass. 
    
    ?patientIDHous rdf:type db:hnscc_clinical_data.tcia_radiomics_id. 
 
    ?ageHous rdf:type db:hnscc_clinical_data.age_at_diag.
    
    ?genderHous rdf:type db:hnscc_clinical_data.gender.
    
    ?hpvHous rdf:type db:hnscc_clinical_data.hpv_status.
    
    ?tumourHous rdf:type db:hnscc_clinical_data.cancer_subsite_of_origin.
    
    ?ajccHous rdf:type db:hnscc_clinical_data.ajcc_stage_7th_edition.
    
    ?tstageHous rdf:type db:hnscc_clinical_data.t_category.
        
    ?nstageHous rdf:type db:hnscc_clinical_data.n_category.
    
    ?rttotaldaysHous rdf:type db:hnscc_clinical_data.radiation_treatment_duration. 
    
    ?graytotaldoseHous rdf:type db:hnscc_clinical_data.total_prescribed_radiation_treatment_dose.
            
    ?graydoseperfractionHous rdf:type db:hnscc_clinical_data.radiation_treatment_dose_per_fraction.
    
    ?rtfractionsHous rdf:type db:hnscc_clinical_data.radiation_treatment_number_of_fractions.
    
    ?survivalHous rdf:type db:hnscc_clinical_data.vital_status.
        
    ?overallsurvivaldaysHous rdf:type db:hnscc_clinical_data.overall_survival_duration.
    
    ?metastasisHous rdf:type db:hnscc_clinical_data.freedom_from_distant_metastasis.
     
    ?localrecurrenceHous rdf:type db:hnscc_clinical_data.local_control.
            
    ?localrecurrencedaysHous rdf:type db:hnscc_clinical_data.local_control_duration.
    
    ?regionalrecurrenceHous rdf:type db:hnscc_clinical_data.regional_control.
    
    ?regionalrecurrencedaysHous rdf:type db:hnscc_clinical_data.regional_control_duration.
    
    ?metastasisdaysHous rdf:type db:hnscc_clinical_data.freedom_from_distant_metastasis_duration.
    
    ?followupHous rdf:type db:hnscc_clinical_data.days_to_last_fu.
    
    ?chemoHous rdf:type db:hnscc_clinical_data.therapeutic_combination. 
}
"""
runQuery(endpoint4, query10)
runQuery(endpoint4, query11)

def addMapping4(localTerm, targetClass, superClass):
    query12 = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX db: <http://hnscc.local/rdf/ontology/>
            PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
            INSERT {
                GRAPH <http://annotation.local/> {
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

    annotationResponse = requests.post(endpoint4,
                                       data="update=" + query12,
                                       headers={
                                           "Content-Type": "application/x-www-form-urlencoded"
                                       })
    print(annotationResponse.status_code)


# T stage
addMapping4("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48719",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping4("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48720",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping4("2", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48724",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping4("3", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48728",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
addMapping4("4", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48732",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")
# addMapping("T4b", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48732", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48885")


# N stage
addMapping4("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48705",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping4("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48706",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping4("2", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")
addMapping4("3", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48714",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48884")

# M stage
addMapping4("0", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48699",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48883")
addMapping4("1", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48700",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48883")

# gender
addMapping4("Female", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C16576",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28421")
addMapping4("Male", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C20197",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28421")

# survival
addMapping4("Dead", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28554",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C25717")
addMapping4("Alive", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C37987",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C25717")
# 0=alive
# 1=dead

# tumorlocation
addMapping4("Base of tongue", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
addMapping4("Tonsil", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
addMapping4("Soft palate", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")
addMapping4("Glossopharyngeal sulcus", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3263")

# hpv
addMapping4("P", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C128839",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")
addMapping4("N", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C131488",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C14226")

# ajcc
addMapping4("I", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27966",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping4("II", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping4("III", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27970",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")
addMapping4("IV", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C38027")

# chemo
# addMapping("chemo radiation", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
addMapping4("Radiation alone", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15313",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
# addMapping("chemo radiation", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
addMapping4("Concurrent chemoradiotherapy", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
addMapping4("Induction chemotherapy%2BRadiation alone", "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")
addMapping4("Induction chemotherapy %2B concurrent chemoradiotherapy",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626",
           "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15632")