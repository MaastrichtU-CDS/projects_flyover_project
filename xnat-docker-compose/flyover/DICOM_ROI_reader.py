from flask import Flask, render_template, request, flash
import requests
import pandas as pd
from io import StringIO
import re

app = Flask(__name__)
app.secret_key = "secret_key"
# enable debugging mode
app.config["DEBUG"] = True


class Cache:
    mydict = {}
    repo = 'userRepo'


v = Cache()


# Root URL
@app.route('/')
def index():
    return render_template('initiate.html')


@app.route("/repo", methods=['POST'])
def queryresult():
    queryROIs = """
    PREFIX db: <https://johanvansoest.nl/ontologies/LinkedDicom/>
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
                select DISTINCT ?ID ?ROI {
                ?patient roo:P100061 ?Subject_label.
                ?Subject_label dbo:has_cell ?subject_cell.
                ?subject_cell dbo:has_value ?ID.
                ?patient roo:has_roi_label ?ROIname.
                ?ROIname dbo:has_cell ?ROIcell.
                ?ROIcell dbo:has_value ?ROI.
    }
    """

    def queryresult(repo, query):
        try:
            endpoint = "http://rdf-store:7200/repositories/" + repo
            annotationResponse = requests.post(endpoint,
                                               data="query=" + query,
                                               headers={
                                                   "Content-Type": "application/x-www-form-urlencoded",
                                                   # "Accept": "application/json"
                                               })
            output = annotationResponse.text
            return output

        except Exception as err:
            flash('Connection unsuccessful. Please check your details!')
            return render_template('initiate.html')

    ROIs = queryresult(v.repo, queryROIs)
    df = pd.read_csv(StringIO(ROIs))
    if 'ROI' in df.columns:
        # roi = df['ROI'].values
        # id = df['ID'].values
        unique_ids = df['ID'].unique()
        id_roi_mapping = {id: df[df['ID'] == id]['ROI'].values.tolist() for id in unique_ids}

        # return render_template('roi.html', id=id, variable=roi)
        return render_template('roi.html', id_roi_mapping=id_roi_mapping)
    print('Connection unsuccessful. Please check your details!')
    return render_template('initiate.html')


@app.route("/rois", methods=['POST'])
def units():
    v.mydict = {}
    for key in request.form:
        if not re.search("^node_", key):
            v.mydict[key] = {}
            if request.form.get(key):
                primary = request.form.get(key)
                v.mydict[key]['primary'] = {}
                v.mydict[key]['primary']['ROI'] = primary
                v.mydict[key]['primary']['URI'] = "http://www.cancerdata.org/roo/C100346"
                equivalencies(v.mydict[key]['primary']['URI'], key, primary)
            if request.form.getlist('node_' + key + '[]'):
                node = request.form.getlist('node_' + key + '[]')
                v.mydict[key]['node'] = {}
                v.mydict[key]['node']['ROI'] = node
                v.mydict[key]['node']['URI'] = "http://www.cancerdata.org/roo/C100347"
                for node_value in node:
                    equivalencies(v.mydict[key]['node']['URI'], key, node_value)

    return render_template('annotation.html')


def equivalencies(URI, key, gtv):
    query = """
        PREFIX db: <https://johanvansoest.nl/ontologies/LinkedDicom/>
        PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
        PREFIX roo: <http://www.cancerdata.org/roo/>
        INSERT
            {
            GRAPH <http://annotations_Dicom/>
            { ?ROIcell dbo:has_code <%s>. }}
        WHERE
            {
            ?patient roo:P100061 ?Subject_label.
            ?Subject_label dbo:has_cell ?subject_cell.
            ?subject_cell dbo:has_value ?ID.
            ?patient roo:has_roi_label ?ROIname.
            ?ROIname dbo:has_cell ?ROIcell.
            ?ROIcell dbo:has_value ?ROI.
            filter contains (?ID, '%s')
            filter contains (?ROI, '%s')
            }
    """ % (URI, key, gtv)

    endpoint = "http://rdf-store:7200/repositories/" + v.repo + "/statements"
    annotationResponse = requests.post(endpoint,
                                       data="update=" + query,
                                       headers={
                                           "Content-Type": "application/x-www-form-urlencoded",
                                           # "Accept": "application/json"
                                       })
    output = annotationResponse.text
    print(output)


if (__name__ == "__main__"):
    # app.run(port = 5001)
    app.run(host='0.0.0.0')
