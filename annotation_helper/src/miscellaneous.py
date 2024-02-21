import json
import logging
import os
import requests

# not a beauty but works; TODO: create a cleaner alternative
_database = 'REPLACEME1'
_variable_definition = "REPLACEME2"
_variable_predicate = "REPLACEME:3"
_variable_class = "REPLACEME:4"

_node_label = "REPLACEME5"
_node_predicate = "REPLACEME:6"
_node_class = "REPLACEME:7"
_node_aesthetic_label = "REPLACEME8"

_class_label = "REPLACEME5"
_class_predicate = "REPLACEME:6"
_class_class = "REPLACEME:7"
_class_aesthetic_label = "REPLACEME8"
_class_iri_label = "REPLACEME9"

string_to_remove = "PREFIX REPLACEME: <>"


def read_file(file_name, path=None):
    """
    Read a file and store its contents

    :param str file_name: name of the file to read
    :param str path: (optional) folder in which the file is located, defaults to current working directory
    :return: contents of the file (string or dictionary)
    """
    # default to current working directory in case no path is specified
    if isinstance(path, str) is False:
        path = os.getcwd()

    file_path = os.path.join(path, file_name)

    # try to read the file and raise an error if unsuccessful
    try:
        logging.debug(f"Reading file {file_path}")
        with open(file_path, 'r') as file:
            if file_name.lower().endswith('.json'):
                # If the file has a .json extension, treat it as a JSON file
                file_contents = json.load(file)
            else:
                # Otherwise, treat it as a text file
                file_contents = file.read()
            return file_contents
    except FileNotFoundError:
        logging.error(f"Error: File '{file_path}' not found.")
    except Exception as e:
        logging.error(f"An error occurred: {e} when attempting to read file '{file_path}'.")


def write_file(file_name, content, path=None, file_extension=None):
    """
    Write content to a file.

    :param str file_name: Name of the file to be written
    :param str content: Content to be written to the file
    :param str path: (optional) Folder in which the file should be saved, defaults to current working directory
    :param str file_extension: (optional) Extension of the file to be written
    """
    # default to the current working directory if no path is specified
    if path is None:
        path = os.getcwd()

    file_path = os.path.join(path, f"{file_name}{file_extension}")

    # try to write to the file and raise an error if unsuccessful
    try:
        logging.debug(f"Writing file {file_path}")
        with open(file_path, 'w') as file:
            file.write(content)
        logging.debug(f"File '{file_path}' successfully written.")
    except Exception as e:
        logging.error(f"An error occurred while writing the file: {e}")


def run_query(queries, endpoint, path=None):
    """
    Read a query from a file and send it on the endpoint with human-readable feedback

    :param list/str queries: filenames that contain the queries to run
    :param str endpoint: endpoint to run the query on
    :param str path: specify a path in which the query file is located
    """
    if isinstance(queries, list):
        # run every query that was specified
        for query in queries:
            _query = read_file(file_name=query, path=path)
            response = __post_query(endpoint=endpoint, query=_query)

            if 200 <= response.status_code < 300:
                logging.info(f"Query: {query} was successfully run on endpoint: {endpoint}; "
                             f"with HTTP response code: {response.status_code}.")
            else:
                logging.warning(f"Query: {query}, was not successfully run on endpoint: {endpoint}.\n"
                                f"HTTP response code: {response.status_code}.")

    elif isinstance(queries, str):
        # run only a single query if not provided as list
        _query = read_file(queries, path=path)
        response = __post_query(endpoint=endpoint, query=_query)

        if 200 <= response.status_code < 300:
            logging.info(f"Query: {queries} was successfully run on endpoint: {endpoint}; "
                         f"with HTTP response code: {response.status_code}.")
        else:
            logging.warning(f"Query: {queries}, was not successfully run on endpoint: {endpoint}.\n"
                            f"HTTP response code: {response.status_code}.")


def add_annotation(endpoint, database, annotation_data, path, remove_has_column=True, save_query=True):
    """
    Add the annotation for a series of variables

    :param str endpoint: endpoint to add the mapping to
    :param str database: database to add the annotation to, e.g., db:'dataset'
    :param dict/str annotation_data: dict with annotation data or path to JSON containing a dict can consist of
    {
    "identifier": {
      "predicate": "roo:P100061",
      "class": "ncit:C25364",
      "local_definition": "research_id"
    },
    "biological_sex": {
      "predicate": "roo:P100018",
      "class": "ncit:C28421",
      "local_definition": "biological_sex",
      "value_mapping": {
        "terms": {
          "male": {
            "local_term": "0",
            "target_class": "ncit:C20197"
          },
          "female": {
            "local_term": "1",
            "target_class": "ncit:C16576"
          }
        }
      }
    },
    "age_at_diagnosis": {
      "predicate": "roo:hasage",
      "class": "ncit:C12345678904",
      "local_definition": "age_at_diagnosis",
      "schema_reconstruction": {
        "type": "node",
        "predicate": "roo:P100027",
        "class": "ncit:C29848",
        "node_label": "years",
        "aesthetic_label": "Years"
      }
    },
    "tumour_type": {
      "predicate": "roo:hastumourtype",
      "class": "ncit:C16899",
      "local_definition": "tumour_type",
      "schema_reconstruction": {
        "type": "class",
        "predicate": "roo:100029",
        "class": "ncit:C3262",
        "class_label": "neoplasmClass",
        "aesthetic_label": "Neoplasm"
      },
      "value_mapping": {
        "terms": {
          "1": {
            "local_term": "1",
            "target_class": "ncit:C16899"
          },
          "2": {
            "local_term": "2",
            "target_class": "ncit:C16899"
          },
          "3": {
            "local_term": "3",
            "target_class": "ncit:C16899"
          }
        }
      }
    }
    }
    :param str path: path to the directory where queries should be saved and where the optional JSON file is located
    :param bool remove_has_column: whether to remove the has_column predicate for cleanliness in the graph
    :param bool save_query: whether to save the query generated for the mapping
    """
    query = None
    construction_query = None
    value_mapping_queries = None

    if isinstance(annotation_data, str) and isinstance(path, str):
        annotation_data = read_file(file_name=annotation_data, path=path)

    if isinstance(annotation_data, dict) is False:
        logging.warning("Annotation data incorrectly formatted, please see function docstring for an example.")
        return None

    for generic_category, variable_data in annotation_data.items():

        # retrieve standard information
        predicate = variable_data.get('predicate')
        class_object = variable_data.get('class')
        local_definition = variable_data.get('local_definition')

        # break the loop if annotation data is not properly defined
        if not all(isinstance(var, str) for var in (predicate, class_object, local_definition)):
            logging.warning(f"Annotation data for variable '{generic_category}' is incorrectly formatted, "
                            f"please see function docstring for an example.")
            break

        # check if schema reconstruction was defined
        reconstruction_data = variable_data.get("schema_reconstruction")
        if isinstance(reconstruction_data, dict):

            # when the reconstruction class is specified as class, create add a class to the datatable
            if "class" in reconstruction_data.get('type'):
                class_predicate = reconstruction_data.get('predicate')
                class_class_object = reconstruction_data.get('class')
                class_label = reconstruction_data.get('class_label')
                class_aesthetic_label = reconstruction_data.get('aesthetic_label')

                # break the loop if schema reconstruction is necessary but not properly defined
                if not all(isinstance(var, str) for var in (
                        class_predicate, class_class_object, class_label, class_aesthetic_label)):
                    logging.warning(
                        f"Schema reconstruction data for variable '{generic_category}' is incorrectly formatted, "
                        "please see function docstring for an example.")
                    break

                # first construct the extra class
                construction_response, construction_query \
                    = _construct_extra_class(endpoint=endpoint,
                                             database_name=database,
                                             class_predicate=class_predicate,
                                             class_class_object=class_class_object,
                                             class_label=class_label,
                                             class_aesthetic_label=class_aesthetic_label.capitalize(),
                                             class_iri_label=class_aesthetic_label.lower())

                # check whether the statement has been added
                construction_success = check_data_class(endpoint=endpoint, database_name=database,
                                                        class_label=class_label,
                                                        variable=generic_category,
                                                        response=construction_response)

                # only proceed if extra class was successfully added
                if construction_success:
                    response, query = _add_annotation_with_extra_class(endpoint=endpoint, variable=generic_category,
                                                                       database_name=database,
                                                                       local_definition=local_definition,
                                                                       predicate=predicate, class_object=class_object,
                                                                       class_predicate=class_predicate,
                                                                       class_class_object=class_class_object,
                                                                       class_label=class_label)

            # when the reconstruction class is specified is node, create a 'hollow' node for the schema
            elif "node" in reconstruction_data.get('type'):
                node_predicate = reconstruction_data.get('predicate')
                node_class_object = reconstruction_data.get('class')
                node_label = reconstruction_data.get('node_label')
                node_aesthetic_label = reconstruction_data.get('aesthetic_label')

                # break the loop if schema reconstruction is necessary but not properly defined
                if not all(isinstance(var, str) for var in (
                        node_predicate, node_class_object, node_label, node_aesthetic_label)):
                    logging.warning(
                        f"Schema reconstruction data for variable '{generic_category}' is incorrectly formatted, "
                        "please see function docstring for an example.")
                    break

                construction_response, construction_query \
                    = _construct_extra_node(endpoint=endpoint, database_name=database, node_label=node_label,
                                            node_aesthetic_label=node_aesthetic_label.capitalize())

                # check whether the statement has been added
                construction_success = check_data_class(endpoint=endpoint, database_name=database,
                                                        class_label=node_label,
                                                        variable=generic_category,
                                                        response=construction_response)

                if construction_success:
                    response, query = _add_annotation_with_extra_node(endpoint=endpoint, variable=generic_category,
                                                                      database_name=database,
                                                                      local_definition=local_definition,
                                                                      predicate=predicate, class_object=class_object,
                                                                      node_predicate=node_predicate,
                                                                      node_class_object=node_class_object,
                                                                      node_label=node_label)

        else:
            # add a standard annotation
            response, query = _add_annotation_standard(endpoint=endpoint, variable=generic_category,
                                                       database_name=database, local_definition=local_definition,
                                                       predicate=predicate, class_object=class_object)

        # check whether the annotation was added successfully
        annotation_success = check_predicate(endpoint=endpoint, predicate=predicate,
                                             variable=generic_category,
                                             response=response)

        # add the value mapping if necessary and possible
        if annotation_success and annotation_data.get('value_mapping'):
            value_mapping_responses, value_mapping_queries = add_mapping(endpoint=endpoint,
                                                                         variable=generic_category,
                                                                         super_class=class_object,
                                                                         value_map=annotation_data[
                                                                             'value_mapping'])

        # remove the 'has_column' section
        if remove_has_column:
            _remove_has_column(endpoint=endpoint, database_name=database, local_definition=local_definition)

        if save_query:
            if os.path.exists(os.path.join(path, 'generated_queries')) is False:
                os.mkdir(os.path.join(path, 'generated_queries'))

            if os.path.exists(os.path.join(path, 'generated_queries', generic_category)) is False:
                os.mkdir(os.path.join(path, 'generated_queries', generic_category))

            write_file(f"{generic_category}", query,
                       os.path.join(path, "generated_queries", generic_category), '.rq')

            if isinstance(construction_query, str):
                write_file(f"{generic_category}_schema_reconstruction", construction_query,
                           os.path.join(path, "generated_queries", generic_category), '.rq')

            if isinstance(value_mapping_queries, list):
                if os.path.exists(os.path.join(path, 'generated_queries', generic_category, "mappings")) is False:
                    os.mkdir(os.path.join(path, 'generated_queries', generic_category, "mappings"))

                for value_mapping_query in value_mapping_queries:
                    write_file(f"{generic_category}_schema_reconstruction", value_mapping_query,
                               os.path.join(path, "generated_queries", generic_category, "mappings"), '.rq')


def add_mapping(endpoint, variable, super_class, value_map):
    """
    Add a mapping between various classes

    :param str endpoint: endpoint to add the mapping to
    :param str variable: variable name for logging purposes
    :param str super_class: class to add the mapping to
    :param dict value_map: dictionary containing the mapping data to save the query generated for the mapping
    """
    responses = []
    queries = []

    if isinstance(value_map.get('terms'), dict):
        for term, term_data in value_map["terms"].items():
            target_class = term_data.get("target_class")
            local_term = term_data.get("local_term")

            if not all(isinstance(var, str) for var in (target_class, local_term)):
                logging.warning(
                    f"Value mapping for term '{term}' of variable '{variable}' is incorrectly formatted, "
                    "please see function docstring for an example.")
                break

            # call your add_mapping function with the appropriate arguments
            response, query = _add_mapping(endpoint=endpoint,
                                           target_class=target_class, super_class=super_class, local_term=local_term)

            # store response and query in list
            responses.append(response)
            queries.append(query)
        return responses, queries
    else:
        logging.warning(f"Value map for variable '{variable}' is incorrectly defined, "
                        f"please see function docstring for an example.")
        return None, None


def check_data_class(endpoint, database_name, class_label, variable, response):
    """
    Check whether a predicate has been added to the endpoint

    :param str endpoint: endpoint to add the mapping to
    :param str database_name: _database to add the annotation to, e.g., db:dataset
    :param str class_label: label to associate with the extra class e.g., neoplasmClass
    :param str variable: variable name for logging purposes
    :param requests.response response: response object from Requests library
    :return:
    """
    if 200 <= response.status_code < 300:
        response, check_query = _check_for_data_class(endpoint=endpoint, database_name=database_name,
                                                      class_label=class_label)
        _response = json.loads(response.text)
        if _response.get('boolean', True) is True:
            logging.info(
                f"Class '{class_label}' was successfully annotated for {variable}.")
            return True

        else:
            logging.warning(
                f"Query for '{variable}' was successfully run on endpoint {endpoint}, "
                f"but class '{class_label}' was not found, consider checking the query.")
            return False

    else:
        logging.warning(
            f"Query for '{variable}', was not successfully run on endpoint: {endpoint}.\n"
            f"HTTP response code: {response.status_code}.")
        return False


def check_predicate(endpoint, predicate, variable, response):
    """
    Check whether a predicate has been added to the endpoint

    :param str endpoint: endpoint to add the mapping to
    :param str predicate: predicate to check
    :param str variable: variable name for logging purposes
    :param requests.response response: response object from Requests library
    :return:
    """
    if 200 <= response.status_code < 300:
        response, check_query = _check_for_predicate(endpoint=endpoint, predicate=predicate)
        _response = json.loads(response.text)
        if _response.get('boolean', True) is True:
            logging.info(
                f"Predicate '{predicate}' was successfully annotated for {variable}.")
            return True

        else:
            logging.warning(
                f"Query for {variable} was successfully run on endpoint {endpoint}, "
                f"but predicate {predicate} was not found, consider checking the query.")
            return False

    else:
        logging.warning(
            f"Query: {variable}, was not successfully run on endpoint: {endpoint}.\n"
            f"HTTP response code: {response.status_code}.")
        return False


def _add_annotation_standard(endpoint, variable, database_name, local_definition, predicate, class_object,
                             template_file=None):
    """
    Directly add a standard annotation

    :param str endpoint: endpoint to add the mapping to
    :param str variable: name of the variable for logging purposes
    :param str database_name: _database to add the annotation to, e.g., db:dataset
    :param str local_definition: variable name to annotate, e.g., biological_sex
    :param str predicate: predicate to associate with the variable
    :param str class_object: class to associate with the variable
    :param str template_file: file name of the template, e.g., src/sparql_templates/template_mapping.rq
    :return: response from request
    """
    logging.debug(f"Adding standard annotation for {variable} to endpoint {endpoint}, database {database_name}")

    if template_file is None:
        template_file = os.path.join(os.getcwd(), "src", "sparql_templates", "template_annotation_standard.rq")

    # retrieve the mapping template
    query = read_file(template_file)

    # replace the components
    replacements = {_database: database_name,
                    _variable_definition: local_definition,
                    _variable_predicate: predicate,
                    _variable_class: class_object}

    for old, new in replacements.items():
        query = query.replace(old, new)

    # remove the prefix for cleanliness
    query.replace(string_to_remove, '')

    # run the query
    response = __post_query(endpoint, query)

    return response, query


def _add_annotation_with_extra_class(endpoint, variable, database_name, local_definition, predicate, class_object,
                                     class_label, class_predicate, class_class_object,
                                     template_file=None):
    """
    Directly add an annotation with an extra class

    :param str endpoint: endpoint to add the mapping to
    :param str variable: name of the variable for logging purposes
    :param str database_name: _database to add the annotation to, e.g., db:dataset
    :param str local_definition: variable name to annotate, e.g., biological_sex
    :param str predicate: predicate to associate with the variable
    :param str class_object: class to associate with the variable
    :param str class_label: label to associate with the extra class e.g., neoplasmClass
    :param str class_predicate: predicate to associate with the extra class
    :param str class_class_object: class to associate with the extra class
    :param str template_file: file name of the template, e.g., src/sparql_templates/template_mapping.rq
    :return: response from request
    """
    logging.debug(f"Adding standard annotation for {variable} to endpoint {endpoint}, database {database_name}")

    if template_file is None:
        template_file = os.path.join(os.getcwd(), "src", "sparql_templates", "template_annotation_with_extra_class.rq")

    # retrieve the mapping template
    query = read_file(template_file)

    # replace the components
    replacements = {_database: database_name,
                    _variable_definition: local_definition,
                    _variable_predicate: predicate,
                    _variable_class: class_object,
                    _class_label: class_label,
                    _class_predicate: class_predicate,
                    _class_class: class_class_object}

    for old, new in replacements.items():
        query = query.replace(old, new)

    # remove the prefix for cleanliness
    query.replace(string_to_remove, '')

    # run the query
    response = __post_query(endpoint, query)

    return response, query


def _add_annotation_with_extra_node(endpoint, variable, database_name, local_definition, predicate, class_object,
                                    node_label, node_predicate, node_class_object,
                                    template_file=None):
    """
    Directly add an annotation with an extra node

    :param str endpoint: endpoint to add the mapping to
    :param str variable: name of the variable for logging purposes
    :param str database_name: _database to add the annotation to, e.g., db:dataset
    :param str local_definition: variable name to annotate, e.g., biological_sex
    :param str predicate: predicate to associate with the variable
    :param str class_object: class to associate with the variable
    :param str node_label: label to associate with the extra class e.g., neoplasmClass
    :param str node_predicate: predicate to associate with the extra class
    :param str node_class_object: class to associate with the extra class
    :param str template_file: file name of the template, e.g., src/sparql_templates/template_mapping.rq
    :return: response from request
    """
    logging.debug(f"Adding standard annotation for {variable} to endpoint {endpoint}, database {database_name}")

    if template_file is None:
        template_file = os.path.join(os.getcwd(), "src", "sparql_templates", "template_annotation_with_extra_node.rq")

    # retrieve the mapping template
    query = read_file(template_file)

    # replace the components
    replacements = {_database: database_name,
                    _variable_definition: local_definition,
                    _variable_predicate: predicate,
                    _variable_class: class_object,
                    _node_label: node_label,
                    _node_predicate: node_predicate,
                    _node_class: node_class_object}

    for old, new in replacements.items():
        query = query.replace(old, new)

    # remove the prefix for cleanliness
    query.replace(string_to_remove, '')

    # run the query
    response = __post_query(endpoint, query)

    return response, query


def _add_mapping(endpoint, target_class, super_class, local_term, template_file=None):
    """
    Directly add a mapping between various classes and data specific term

    :param str endpoint: endpoint to add the mapping to
    :param str target_class: specific class, e.g., male or female
    :param str super_class: overarching class, e.g., biological sex
    :param str local_term: a value in the data e.g, 0 for female and 1 for male
    :param str template_file: file name of the mapping template, e.g., template_mapping.rq
    :return: response from request
    """
    logging.debug(f"Adding mapping for {super_class} to endpoint {endpoint}")

    if template_file is None:
        template_file = os.path.join(os.getcwd(), "src", "sparql_templates", "template_mapping.rq")

    # retrieve the mapping template
    mapping_template = read_file(template_file)

    # add the target_class, super_class, and local_term
    mapping_query = mapping_template % (target_class, super_class, local_term)

    # run the query
    response = __post_query(endpoint, mapping_query)

    return response, mapping_query


def _check_for_data_class(endpoint, database_name, class_label, template_file=None):
    """
    Check whether a statement has been added

    :param str endpoint: endpoint to add the mapping to
    :param str database_name: predicate to check whether present
    :param str template_file: file name of the template, e.g., src/sparql_templates/template_mapping.rq
    :return: response from request
    """
    if template_file is None:
        template_file = os.path.join(os.getcwd(), "src", "sparql_templates", "template_to_check_class.rq")

    # retrieve the mapping template
    query = read_file(template_file)

    # replace the placeholders
    replacements = {_database: database_name,
                    _class_label: class_label}

    for old, new in replacements.items():
        query = query.replace(old, new)

    # remove the prefix for cleanliness
    query.replace(string_to_remove, '')

    # run the query
    response = __post_query(endpoint=endpoint.rsplit('/statements', 1)[0], query=query,
                            data_style=f"query=" + query)

    return response, query


def _check_for_predicate(endpoint, predicate, template_file=None):
    """
    Check whether a statement has been added

    :param str endpoint: endpoint to add the mapping to
    :param str predicate: predicate to check whether present
    :param str template_file: file name of the template, e.g., src/sparql_templates/template_mapping.rq
    :return: response from request
    """
    if template_file is None:
        template_file = os.path.join(os.getcwd(), "src", "sparql_templates", "template_to_check_predicate.rq")

    # retrieve the mapping template
    query = read_file(template_file)

    # replace the placeholder
    query = query.replace(_variable_predicate, predicate)

    # remove the prefix for cleanliness
    query.replace(string_to_remove, '')

    # run the query
    response = __post_query(endpoint=endpoint.rsplit('/statements', 1)[0], query=query,
                            data_style=f"query=" + query)

    return response, query


def _construct_extra_class(endpoint, database_name, class_label, class_predicate, class_class_object,
                           class_aesthetic_label, class_iri_label,
                           template_file=None):
    """
    Directly add an annotation with an extra class

    :param str endpoint: endpoint to add the mapping to
    :param str database_name: _database to add the annotation to, e.g., db:dataset
    :param str class_label: label to associate with the extra class e.g., neoplasmClass
    :param str class_predicate: predicate to associate with the extra class
    :param str class_class_object: class to associate with the extra class
    :param str class_aesthetic_label: label to associate with the extra class, e.g., Neoplasm
    :param str class_iri_label: iri label to associate with the extra class e.g., neoplasm
    :param str template_file: file name of the template, e.g., src/sparql_templates/template_mapping.rq
    :return: response from request
    """
    logging.debug(f"Constructing extra {class_label} to endpoint {endpoint}, database {database_name}")

    if template_file is None:
        template_file = os.path.join(os.getcwd(), "src", "sparql_templates",
                                     "template_reconstruction_with_extra_class.rq")

    # retrieve the mapping template
    query = read_file(template_file)

    # replace the components
    replacements = {_database: database_name,
                    _class_label: class_label,
                    _class_predicate: class_predicate,
                    _class_class: class_class_object,
                    _class_aesthetic_label: class_aesthetic_label,
                    _class_iri_label: class_iri_label}

    for old, new in replacements.items():
        query = query.replace(old, new)

    # remove the prefix for cleanliness
    query.replace(string_to_remove, '')

    # run the query
    response = __post_query(endpoint, query)

    return response, query


def _construct_extra_node(endpoint, database_name, node_label, node_aesthetic_label, template_file=None):
    """
    Add an extra node that can be used to associate to an actual variable

    :param str endpoint: endpoint to add the mapping to
    :param str database_name: _database to add the annotation to, e.g., db:dataset
    :param str node_label: label to associate with the extra class e.g., neoplasmClass
    :param str node_aesthetic_label: label to associate with the extra class, e.g., Neoplasm
    :param str template_file: file name of the template, e.g., src/sparql_templates/template_mapping.rq
    :return: response from request
    """
    logging.debug(f"Adding extra node for {node_label} to endpoint {endpoint}, database {database_name}")

    if template_file is None:
        template_file = os.path.join(os.getcwd(), "src", "sparql_templates",
                                     "template_reconstruction_with_extra_node.rq")

    # retrieve the mapping template
    query = read_file(template_file)

    # replace the components
    replacements = {_database: database_name,
                    _node_label: node_label,
                    _node_aesthetic_label: node_aesthetic_label}

    for old, new in replacements.items():
        query = query.replace(old, new)

    # remove the prefix for cleanliness
    query.replace(string_to_remove, '')

    # run the query
    response = __post_query(endpoint, query)

    return response, query


def _remove_has_column(endpoint, database_name, local_definition, template_file=None):
    """
    Directly add an annotation with an extra node

    :param str endpoint: endpoint to add the mapping to
    :param str database_name: _database to add the annotation to, e.g., db:dataset
    :param str local_definition: variable name to annotate, e.g., biological_sex
    :param str template_file: file name of the template, e.g., src/sparql_templates/template_mapping.rq
    :return: response from request
    """
    logging.debug(f"Remove has_column for {local_definition} on endpoint {endpoint}, database {database_name}")

    if template_file is None:
        template_file = os.path.join(os.getcwd(), "src", "sparql_templates", "template_remove_has_column.rq")

    # retrieve the mapping template
    query = read_file(template_file)

    # replace components
    replacements = {_database: database_name,
                    _variable_definition: local_definition}

    for old, new in replacements.items():
        query = query.replace(old, new)

    # remove the prefix for cleanliness
    query.replace(string_to_remove, '')

    # run the query
    response = __post_query(endpoint, query)

    return response, query


def __post_query(endpoint, query, headers=None, data_style=None):
    """
    Run a query and return the response

    :param str endpoint: endpoint to post the provided query to
    :param str query: query that is posted to the provided endpoint
    :param dict headers: provide the headers to use when posting request
    e.g.,  {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}
    :return:
    """
    if isinstance(headers, dict) is False:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

    if isinstance(data_style, str) is False:
        data_style = "update=" + query

    annotation_response = requests.post(endpoint, data=data_style, headers=headers)

    return annotation_response
