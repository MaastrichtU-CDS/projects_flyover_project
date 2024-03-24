import copy
import json
import os
import re
import requests
import shutil
import subprocess

import pandas as pd

from flask import abort, Flask, render_template, request, flash, Response
from io import StringIO
from psycopg2 import connect
from werkzeug.utils import secure_filename

# Change these names
graphdb_url = "http://rdf-store:7200"

app = Flask(__name__)
app.secret_key = "secret_key"
# enable debugging mode
app.config["DEBUG"] = True
UPLOAD_FOLDER = os.path.join('static', 'files')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


class Cache:
    def __init__(self):
        self.repo = 'userRepo'
        self.file_path = None
        self.table = None
        self.url = None
        self.username = None
        self.password = None
        self.db_name = None
        self.conn = None
        self.col_cursor = None
        self.csvPath = False
        self.uploaded_file = None
        self.global_schema = None
        self.global_schema_path = None


session_cache = Cache()


# Root URL
@app.route('/')
def index():
    """
    This function renders the index.html page

    :return:
    """
    return render_template('index.html')


def allowed_file(filename, allowed_extensions):
    """
    This function checks if the uploaded file has an allowed extension.

    Parameters:
    filename (str): The name of the file to be checked.
    allowed_extensions (set): A set of strings representing the allowed file extensions.

    Returns:
    bool: True if the file has an allowed extension, False otherwise.
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions


def file_upload_and_save(file_type):
    # check if the upload folder is writable
    if not os.access(app.config['UPLOAD_FOLDER'], os.W_OK):
        flash("No write access to the upload folder. Exiting.")
        return render_template('index.html')

    session_cache.uploaded_file = request.files.get(file_type)

    filename = secure_filename(session_cache.uploaded_file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        session_cache.uploaded_file.save(file_path)
        return file_path
    except Exception as e:
        flash(f'Failed to save the {file_type} file. Error: {e}')
        return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    This function handles the file upload process.
    It accepts JSON and CSV files, and also handles data from a PostgreSQL database.

    The function works as follows:
    1. It retrieves the file type, JSON file, and CSV file from the form data.
    2. If a JSON file is provided and its file extension is allowed, it uploads and saves the file,
     and stores the file path in the session cache.
    3. If the file type is 'CSV' and a CSV file is provided and its file extension is allowed,
    it uploads and saves the file, stores the file path in the session cache, and runs the triplifier.
    4. If the file type is 'Postgres', it handles the PostgreSQL data using the provided username, password, URL,
     database name, and table name, and runs the triplifier.
    5. It returns a response indicating whether the triplifier run was successful.

    Returns:
        flask.Response: A Flask response object containing the rendered 'triples.html' template if the triplifier run was successful, or the 'index.html' template if it was not.
    """
    file_type = request.form.get('fileType')
    json_file = request.files.get('jsonFile')
    csv_file = request.files.get('csvFile')

    if json_file:
        if allowed_file(json_file.filename, {'json'}) is False:
            flash("If opting to submit a global schema, please upload it as a '.json' file.")
            return render_template('index.html', error=True)

        session_cache.global_schema_path = file_upload_and_save('jsonFile')

    if file_type == 'CSV' and csv_file:
        if allowed_file(csv_file.filename, {'csv'}) is False:
            flash("If opting to submit a CSV data source, please upload it as a '.csv' file.")
            return render_template('index.html', error=True)
        session_cache.csvPath = file_upload_and_save('csvFile')
        success, message = run_triplifier()
    elif file_type == 'Postgres':
        handle_postgres_data(request.form.get('username'), request.form.get('password'),
                             request.form.get('POSTGRES_URL'), request.form.get('POSTGRES_DB'),
                             request.form.get('table'))
        success, message = run_triplifier()

    if success:
        return render_template('triples.html', variable=message)
    else:
        flash(f"Attempting to run the Triplifier resulted in an error: {message}")
        return render_template('index.html', error=True)


def run_triplifier():
    """
    This function runs the triplifier and checks if it ran successfully.

    Returns:
        tuple: A tuple containing a boolean indicating if the triplifier ran successfully, and a string containing the error message if it did not.
    """
    try:
        process = subprocess.Popen("java -jar /app/data_descriptor/javaTool/triplifier.jar -p /app/data_descriptor/triplifierCSV.properties",
                                   shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # Print the output to the terminal
        output, _ = process.communicate()
        output = output.decode()
        print(output)

        if process.returncode == 0:
            return True, "Triplifier ran successfully!"
        else:
            return False, output
    except Exception as err:
        return False, str(err)


def handle_postgres_data(username, password, postgres_url, postgres_db, table):
    """
    This function handles the PostgreSQL data. It caches the provided information, establishes a connection to the PostgreSQL database, and writes the connection details to a properties file.

    Parameters:
    username (str): The username for the PostgreSQL database.
    password (str): The password for the PostgreSQL database.
    postgres_url (str): The URL of the PostgreSQL database.
    postgres_db (str): The name of the PostgreSQL database.
    table (str): The name of the table in the PostgreSQL database.

    Returns:
    flask.Response: A Flask response object containing the rendered 'index.html' template if the connection to the PostgreSQL database fails.
    None: If the connection to the PostgreSQL database is successful.
    """
    # Cache information
    session_cache.username, session_cache.password, session_cache.url, session_cache.db_name, session_cache.table = username, password, postgres_url, postgres_db, table

    try:
        # Establish PostgreSQL connection
        session_cache.conn = connect(dbname=session_cache.db_name, user=session_cache.username,
                                     host=session_cache.url,
                                     password=session_cache.password)
        print("Connection:", session_cache.conn)
    except Exception as err:
        print("connect() ERROR:", err)
        session_cache.conn = None
        flash('Attempting to connect to PostgreSQL datasource unsuccessful. Please check your details!')
        return render_template('index.html', error=True)

    # Write connection details to properties file
    with open("/app/data_descriptor/triplifierSQL.properties", "w") as f:
        f.write(f"jdbc.url = jdbc:postgresql://{session_cache.url}/{session_cache.db_name}\n"
                f"jdbc.user = {session_cache.username}\n"
                f"jdbc.password = {session_cache.password}\n"
                f"jdbc.driver = org.postgresql.Driver\n\n"
                f"repo.type = rdf4j\n"
                f"repo.url = {graphdb_url}\n"
                f"repo.id = userRepo")


# Get the uploaded files
@app.route("/repo", methods=['POST'])
def queryresult():
    queryColumn = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
        select ?o where { 
        ?s dbo:column ?o .
    }
    """

    def queryresult(repo, query):
        try:
            endpoint = f"{graphdb_url}/repositories/" + repo
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
            return render_template('index.html')

    columns = queryresult(session_cache.repo, queryColumn)
    local_column_names = pd.read_csv(StringIO(columns))
    local_column_names = local_column_names[local_column_names.columns[0]]

    # if a global schema was defined, read it
    if isinstance(session_cache.global_schema_path, str) is False:
        global_names = ['Research subject identifier', 'Biological sex', 'Age at inclusion', 'Other']
        session_cache.global_schema = None
    else:
        try:
            with open(session_cache.global_schema_path, 'r') as file:
                session_cache.global_schema = json.load(file)

            # get the global variable names
            global_names = [global_name.capitalize().replace('_', ' ')
                            for global_name in session_cache.global_schema['variable_info'].keys()]

            # add an option to select 'Other'
            global_names.append('Other')
        except FileNotFoundError:
            print("Global schema file not found")

        except json.JSONDecodeError:
            print("Global schema has an invalid JSON format")

    return render_template('categories.html', local_variable_names=local_column_names,
                           global_variable_names=global_names)


@app.route("/units", methods=['POST'])
def units():
    conList = []
    session_cache.mydict = {}
    for local_variable_name in request.form:
        if not re.search("^ncit_comment_", local_variable_name):
            session_cache.mydict[local_variable_name] = {}
            data_type = request.form.get(local_variable_name)
            global_variable_name = request.form.get('ncit_comment_' + local_variable_name)
            comment = request.form.get('comment_' + local_variable_name)
            session_cache.mydict[local_variable_name]['type'] = data_type
            session_cache.mydict[local_variable_name]['description'] = global_variable_name
            session_cache.mydict[local_variable_name]['comments'] = comment
            if data_type == 'Categorical Nominal' or data_type == 'Categorical Ordinal':
                cat = getCategories(session_cache.repo, local_variable_name)
                TESTDATA = StringIO(cat)
                df = pd.read_csv(TESTDATA, sep=",")
                df = df.to_dict('records')
                session_cache.mydict[local_variable_name]['categories'] = df
                equivalencies(session_cache.mydict, local_variable_name)
            elif data_type == 'Continuous':
                conList.append(local_variable_name)
            else:
                equivalencies(session_cache.mydict, local_variable_name)

    return render_template('units.html', variable=conList)


def getCategories(repo, key):
    queryCategories = """
        PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
        PREFIX db: <http://'%s'.local/rdf/ontology/>
        PREFIX roo: <http://www.cancerdata.org/roo/>
        SELECT ?value (COUNT(?value) as ?count)
        WHERE 
        {  
           ?a a ?v.
           ?v dbo:column '%s'.
           ?a dbo:has_cell ?cell.
           ?cell dbo:has_value ?value
        } groupby(?value)
        """ % (repo, key)

    endpoint = f"{graphdb_url}/repositories/" + repo
    annotationResponse = requests.post(endpoint,
                                       data="query=" + queryCategories,
                                       headers={
                                           "Content-Type": "application/x-www-form-urlencoded",
                                           # "Accept": "application/json"
                                       })
    output = annotationResponse.text
    return output


@app.route("/end", methods=['POST'])
def unitNames():
    # items = getColumns(file_path)
    for key in request.form:
        unitValue = request.form.get(key)
        if unitValue != "":
            session_cache.mydict[key]['units'] = unitValue
        equivalencies(session_cache.mydict, key)

    # try to fetch the global schema if it was read previously
    if isinstance(session_cache.global_schema, dict) and isinstance(session_cache.mydict, dict):
        return render_template('download.html',
                               graphdb_location="http://localhost:7200/", show_schema=True)
    else:
        return render_template('download.html',
                               graphdb_location="http://localhost:7200/", show_schema=False)


@app.route('/downloadSchema', methods=['GET'])
def download_schema(filename='local_schema.json'):
    """
    This function generates a modified version of the global schema by adding local definitions to it.
    The modified schema is then returned as a JSON response which can be downloaded as a file.

    Parameters:
    filename (str): The name of the file to be downloaded. Defaults to 'local_schema.json'.

    Returns:
        flask.Response: A Flask response object containing the modified schema as a JSON string.
                        If an error occurs during the processing of the schema,
                        an HTTP response with a status code of 500 (Internal Server Error)
                        is returned along with a message describing the error.
    """
    try:
        modified_schema = copy.deepcopy(session_cache.global_schema)

        for local_variable, local_value in session_cache.mydict.items():
            global_variable = local_value['description'].lower().replace(' ', '_')
            if global_variable:
                modified_schema['variable_info'][global_variable]['local_definition'] = local_variable

        return Response(json.dumps(modified_schema, indent=4),
                        mimetype='application/json',
                        headers={'Content-Disposition': f'attachment;filename={filename}'})
    except Exception as e:
        abort(500, description=f"An error occurred while processing the schema, error: {str(e)}")


@app.route('/downloadOntology', methods=['GET'])
def download_ontology(named_graph="http://ontology.local/", filename='local_ontology.nt'):
    """
    This function downloads an ontology from a specified graph and returns it as a response which
    can be downloaded as a file.

    Parameters:
    named_graph (str): The URL of the graph from which the ontology is to be downloaded.
    Defaults to "http://ontology.local/".
    filename (str): The name of the file to be downloaded. Defaults to 'local_ontology.nt'.

    Returns:
        flask.Response: A Flask response object containing the ontology as a string if the download is successful,
                        or an error message if the download fails.
                        If an error occurs during the processing of the request,
                        an HTTP response with a status code of 500 (Internal Server Error)
                         is returned along with a message describing the error.
    """
    try:
        response = requests.get(
            f"{graphdb_url}/repositories/{session_cache.repo}/rdf-graphs/service",
            params={"graph": named_graph},
            headers={"Accept": "application/n-triples"}
        )

        if response.status_code == 200:
            return Response(response.text,
                            mimetype='application/n-triples',
                            headers={'Content-Disposition': f'attachment;filename={filename}'})

    except Exception as e:
        abort(500, description=f"An error occurred while processing the ontology, error: {str(e)}")


def equivalencies(mydict, key):
    query = """
        PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
        PREFIX db: <http://%s.local/rdf/ontology/>
        PREFIX roo: <http://www.cancerdata.org/roo/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        INSERT  
            {
            GRAPH <http://ontology.local/>
            { ?s owl:equivalentClass "%s". }}
        WHERE 
            {
            ?s dbo:column '%s'.
            }        
    """ % (session_cache.repo, list(mydict[key].values()), key)

    endpoint = f"{graphdb_url}/repositories/" + session_cache.repo + "/statements"
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
