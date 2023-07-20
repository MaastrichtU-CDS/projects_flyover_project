# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 11:37:13 2021

@author: leonard.wee
"""

import pydicom as dicom
import os
#import re
import shutil

homeFolder = 'C:/somewhere' #CHANGE THIS PATH!
#backupFolder = 'C:/decompress2'

listOfFiles = [os.path.join(dp, f) for dp, dn, filenames in os.walk(homeFolder) for f in filenames if not f.startswith('.')]

for ff in listOfFiles:
    try:
        this = dicom.dcmread(ff, force=True)
        patid=this.PatientID
        path = backupFolder + '/' + patid
        #does the folder exist?
        if not (os.path.isdir(path)):
            os.makedirs(path)
        #make new path
        fn = os.path.basename(ff) #the base file name
        if (this.Modality == "CT"):
            this.decompress()
            this.save_as(os.path.join(path, fn))
        else:
            shutil.copyfile(ff, os.path.join(path, fn))
            #shutil.move(ff, os.path.join(rtstructsBackup, fn))
    except:
        pass


