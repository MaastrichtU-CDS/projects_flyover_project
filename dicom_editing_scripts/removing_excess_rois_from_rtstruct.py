# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 18:08:00 2020
 
@author: Leonard Wee
"""
 
 
import pydicom as dicom
import os
#import pandas as pd
#from decimal import Decimal
import re
 
 
"""
# use this code CAUTIOUSLY as it will help you delete unwanted structures
# automatically from any RTSTRUCT file that it finds.
#
# works on the basis of regular expressions (REGEX) text matching, so please seek
# guidance about REGEX or do a test on your own before using in full batch mode
#
# you may adjust lines 46, 50, 54, ..., etc. below to suit your needs
# this example is looking for any ROI that matched the external skin outline
# or the treatment couch or the body contour, and will delete those
#
# if you need more, uncomment the remaining lines then adjust the REGEX term that you seek
"""

folderPath = 'C:/somewhere' #CHANGE ME!
 
listOfFiles = [os.path.join(dp, f) for dp, dn, filenames in os.walk(folderPath) for f in filenames if not f.startswith('.')]
 
f = open(folderPath+'/rois_audit.txt',"w")
 
for ff in listOfFiles:
    try:
        this = dicom.read_file(ff,force=True)
        if this.Modality=='RTSTRUCT':
            for i in range( len(this.StructureSetROISequence)-1,-1,-1 ):
                if re.search(r'[Ee]xternal',this.StructureSetROISequence[i].ROIName):
                    del this.StructureSetROISequence[i]
                    del this.ROIContourSequence[i]
                    del this.RTROIObservationsSequence[i]
                elif re.search(r'^[Cc]ouch',this.StructureSetROISequence[i].ROIName):
                    del this.StructureSetROISequence[i]
                    del this.ROIContourSequence[i]
                    del this.RTROIObservationsSequence[i]
                elif re.search(r'^[Bb]ody',this.StructureSetROISequence[i].ROIName):
                    del this.StructureSetROISequence[i]
                    del this.ROIContourSequence[i]
                    del this.RTROIObservationsSequence[i]
#                elif re.search(r'hot',this.StructureSetROISequence[i].ROIName):
#                    del this.StructureSetROISequence[i]
#                    del this.ROIContourSequence[i]
#                    del this.RTROIObservationsSequence[i]
#                elif re.search(r'^Liver',this.StructureSetROISequence[i].ROIName):
#                    del this.StructureSetROISequence[i]
#                    del this.ROIContourSequence[i]
#                    del this.RTROIObservationsSequence[i]
#                elif re.search(r'^ICD',this.StructureSetROISequence[i].ROIName):
#                    del this.StructureSetROISequence[i]
#                    del this.ROIContourSequence[i]
#                    del this.RTROIObservationsSequence[i]
#                elif re.search(r'^[Pp]acemaker',this.StructureSetROISequence[i].ROIName):
#                    del this.StructureSetROISequence[i]
#                    del this.ROIContourSequence[i]
#                    del this.RTROIObservationsSequence[i]
#                elif re.search(r'^Plex',this.StructureSetROISequence[i].ROIName):
#                    del this.StructureSetROISequence[i]
#                    del this.ROIContourSequence[i]
#                    del this.RTROIObservationsSequence[i]
#                elif re.search(r'^scatter',this.StructureSetROISequence[i].ROIName):
#                    del this.StructureSetROISequence[i]
#                    del this.ROIContourSequence[i]
#                    del this.RTROIObservationsSequence[i]
                else:
                    #print(this.PatientID, this.StructureSetROISequence[i].ROIName, sep=";", file=f)
                    print(this.PatientID, this.StructureSetROISequence[i].ROIName)
            this.save_as(ff)
    except:
        pass
 
f.close()
