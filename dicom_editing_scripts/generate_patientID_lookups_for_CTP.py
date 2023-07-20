# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 15:54:02 2021
 
@author: Leonard Wee
"""
 
""""
#
# Iterate through a folder of DICOM files and generate the patient ID lookup table needed for CTP
# As by-product I also provide a text file listing every ROI that has been found
# Upon conclusion, you may copy-paste the contents of the temp_lookup file into
# your own Clinical Trial Processor patient ID lookup table, as per the readme instructions
# in that part of the gitlab repository
#
# you may chnage line 24 and line 64 to fit your own needs
#
"""
import pydicom as dicom
import os
import pandas as pd
 
 
homeFolder = "C:/something" #CHANGE THIS!
patientIDfile = homeFolder + "/patient_id_file.txt" #these lines define the path to the output of script
roiListFile = homeFolder + "/roi_names_file.txt" #these lines define the path to the output of script
lookupTemp = homeFolder + "/temp_lookup.txt" #these lines define the path to the output of script
 
#descends into the target folder and lists everything that it finds which is not a hidden file
listOfFiles = [os.path.join(dp, f) for dp, dn, filenames in os.walk(homeFolder) for f in filenames if not f.startswith('.')]
 
#open some files to write contents into
writePatid = open(patientIDfile,"w")
writeRois = open(roiListFile,"w")
 
#main loop to write out all the patients IDs and ROI names found
for ff in listOfFiles:
    try:
        this = dicom.dcmread(ff)
        if this.Modality=="RTSTRUCT":
            rois=this.StructureSetROISequence
            for r in rois:
                print(this.PatientID + ',' + r.ROIName, file=writeRois)
        elif this.Modality=="CT":
            patid = this.PatientID
            print("ptid/"+patid+",0", file=writePatid)
        else:
            pass
    except:
        pass                
writePatid.close()
writeRois.close()
 
#now imports the patient IDs file as a pandas dataframe, removes duplicates
#then assignes a new research Identifier to each line
#results in a Clinical Trial Processor kind of format that is easy to copy and paste
df = pd.read_csv(patientIDfile, header=None)
df.drop_duplicates(inplace=True)
 
#create a list of fixed length number strings, as many as there are unique IDs
lines = df[0].tolist()
writeLookup = open(lookupTemp,"w")
for i in range(0,len(lines)):
    print(lines[i]+'=MyData-{0:04d}'.format(i+1), file=writeLookup) #CHANGE MyData to whatever word you want
writeLookup.close()
 
 
