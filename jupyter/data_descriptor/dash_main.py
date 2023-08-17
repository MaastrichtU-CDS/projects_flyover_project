import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import requests
from io import StringIO
import time

queryT = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?tstage
    WHERE {
    OPTIONAL
    {
        ?tablerow roo:P100029 ?neoplasm.
        ?neoplasm roo:P100244 ?tstagev.
        ?tstagev dbo:has_cell ?cell.
        ?cell a ?t.
        FILTER regex(str(?t), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48719|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48720|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48724|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48728|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48732"))
        BIND(strafter(str(?t), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?tstage)
    }
    }
            """

queryG = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?gender
    WHERE {
    OPTIONAL
    {
        ?tablerow roo:P100018 ?genderv.
        ?genderv dbo:has_cell ?cell.
        ?cell a ?g.
        FILTER regex(str(?g), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C16576|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C20197"))
        BIND(strafter(str(?g), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?gender)
    }
}
"""
queryN = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?nstage
    WHERE {
    OPTIONAL
    {
        ?tablerow roo:P100029 ?neoplasm.
        ?neoplasm roo:P100242 ?nstagev.
        ?nstagev dbo:has_cell ?cell.
        ?cell a ?n.
        FILTER regex(str(?n), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48705|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48706|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48714"))
        BIND(strafter(str(?n), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?nstage)
    }
    }
"""
queryM = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?mstage
    WHERE {
    OPTIONAL
    {
        ?tablerow roo:P100029 ?neoplasm.
        ?neoplasm roo:P100241 ?mstagev.
        ?mstagev dbo:has_cell ?cell.
        ?cell a ?m.
        FILTER regex(str(?m), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48699|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48700"))
        BIND(strafter(str(?m), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?mstage)
    }
    }
"""
queryS = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?survival
    WHERE {
    OPTIONAL
    {
        ?tablerow roo:P100254 ?survivalv.
        ?survivalv dbo:has_cell ?cell.
        ?cell a ?s.
        FILTER regex(str(?s), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28554|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C37987"))
        BIND(strafter(str(?s), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?survival)
    }
    }
"""
queryAge = """
	PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?agevalue   
    WHERE 
        {
        ?tablerow roo:hasage ?age.
        ?age dbo:has_cell ?cell.
        ?cell roo:P100042 ?agevalue.  
	}
"""
queryAjccSex = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?Gender ?AJCC ?TumourLocation
    WHERE {
    ?tablerow roo:P100018 ?genderv.
    ?tablerow roo:P100029 ?neoplasm.
    ?neoplasm roo:P100219 ?ajccv.
    ?neoplasm roo:P100202 ?tumourv.

    ?genderv dbo:has_cell ?gendercell.
    ?ajccv dbo:has_cell ?ajcccell.
    ?tumourv dbo:has_cell ?tumourcell.

    ?gendercell a ?g.
    ?ajcccell a ?a.
    ?tumourcell a ?t.

    FILTER regex(str(?g), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C16576|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C20197"))
    FILTER regex(str(?a), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27966|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27970|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971"))
    FILTER regex(str(?t), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12246|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12420|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12423"))

    BIND(strafter(str(?g), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?Gender)
    BIND(strafter(str(?a), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?AJCC)
    BIND(strafter(str(?t), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?TumourLocation)
}
"""
queryAjcc = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?ajcc
    WHERE {
    OPTIONAL {
    ?tablerow roo:P100029 ?neoplasm.
    ?neoplasm roo:P100219 ?ajccv.
    ?ajccv dbo:has_cell ?ajcccell.
    ?ajcccell a ?a.
    FILTER regex(str(?a), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27966|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27970|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971"))
    BIND(strafter(str(?a), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?ajcc)   
    } 
}
"""
queryTumour = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?TumourLocation
    WHERE {
    OPTIONAL {
    ?tablerow roo:P100029 ?neoplasm.
    ?neoplasm roo:P100202 ?tumour. 
    ?tumour dbo:has_cell ?tumourcell. 
    ?tumourcell a ?t.
    FILTER regex(str(?t), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12246|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12420|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12423"))
    BIND(strafter(str(?t), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?TumourLocation)
    }
}
"""
queryHpv = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?hpv
    WHERE {
    OPTIONAL {
    ?tablerow roo:P100022 ?hpvv.
    ?hpvv dbo:has_cell ?hpvcell.
    ?hpvcell a ?h.
    FILTER regex(str(?h), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C128839|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C131488"))
    BIND(strafter(str(?h), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?hpv)
   }
}
"""
queryChemo = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?therapy
    WHERE {
    OPTIONAL {
    ?tablerow roo:P100231 ?chemov.
    ?chemov dbo:has_cell ?chemocell.
    ?chemocell a ?c.
    FILTER regex(str(?c), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15313"))
    BIND(strafter(str(?c), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?therapy)
   }
}
"""
def queryresult(repo, query):
    endpoint = "http://rdf-store:7200/repositories/" + repo
    annotationResponse = requests.post(endpoint,
                                       data="query=" + query,
                                       headers={
                                           "Content-Type": "application/x-www-form-urlencoded",
                                           # "Accept": "application/json"
                                       })
    output = annotationResponse.text
    return output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div([
    html.H5("Repository name:"),
    dcc.Input(id='userRepo', placeholder='Enter the repository name here...',
              value=None, type='text',
              style=dict(display='flex', justifyContent='center')),

    dcc.Loading(
        id="loading-2",
        children=[html.Div([html.Div(id="loading-output-2")])],
        type="default"
    ),
    html.Div(children=[
        dcc.Graph(id="sunburst", style={"width": 800, "margin": 0, 'display': 'inline-block'}),
        dcc.Graph(id="scatter", style={"width": 400, "margin": 0, 'display': 'inline-block'}),
        #dcc.Graph(id="box"),
    ]),
    html.Div([
        html.H5("Choose an option:"),
        dcc.Dropdown(
            id='columns',
            value='gender',
            options=[{'label': 'Gender', 'value': 'gender'},
                     {'label': 'T stage', 'value': 'tstage'},
                     {'label': 'N stage', 'value': 'nstage'},
                     {'label': 'M stage', 'value': 'mstage'},
                     {'label': 'Survival Status', 'value': 'survival'},
                     {'label': 'HPV Status', 'value': 'hpv'},
                     {'label': 'AJCC Stage', 'value': 'ajcc'},
                     {'label': 'Tumour Location', 'value': 'TumourLocation'},
                     {'label': 'Therapy given', 'value': 'therapy'}, ],
            clearable=False,
            style={'width': '220px'}),
        html.Div(children=[
            dcc.Graph(id="pie-chart")]),

    ])
])

result_userRepo = pd.DataFrame()

codedict = {
        "C16576": "Female", "C20197": "Male", "C27966": "Stage I", "C28054": "Stage II",
        "C27970": "Stage III", "C27971": "Stage IV", "C12762": "Oropharynx", "C12420": "Larynx",
        "C12246": "Hypopharynx", "C12423": "Nasopharynx", "C48719": "T0", "C48720": "T1", "C48724": "T2",
        "C48728": "T3", "C48732": "T4", "C48705": "N0", "C48706": "N1", "C48786": "N2", "C48714": "N3",
        "C48699": "M0", "C48700": "M1", "C28554": "Dead", "C37987": "Alive", "C128839": "HPV Positive",
        "C131488": "HPV Negative", "C94626": "ChemoRadiotherapy", "C15313": "Radiotherapy"
    }

@app.callback(
    Output("sunburst", "figure"),
    [Input("userRepo", "value"),
     Input("columns", "value")])
def update_sun(userRepo, columns):
    result = pd.DataFrame()
    if userRepo:
        url = "http://rdf-store:7200/repositories/" + userRepo
        if (requests.head(url).status_code)==400:
            result_data = queryresult(userRepo, queryAjccSex)
            userRepodata = pd.read_csv(StringIO(result_data))
            for col in userRepodata.columns:
                userRepodata[col] = userRepodata[col].map(codedict).fillna(userRepodata[col])
            result = userRepodata
            # print(result)
            if (result.empty == False):
                fig = px.sunburst(result, path=['Gender', 'AJCC', 'TumourLocation'], color='AJCC')
                fig.update_layout(title_text='Gender & Stage-wise Tumour Location', title_x=0.5)
                return fig
            else:
                fig = px.sunburst(None)
                return fig
        else:
            fig = px.sunburst(None)
            return fig
    else:
        fig = px.scatter(None)
        return fig

@app.callback(
    Output("scatter", "figure"),
    [Input("userRepo", "value"),
     Input("columns", "value")])
def update_scatter(userRepo, columns):
    result = pd.DataFrame()
    if userRepo:
        url = "http://rdf-store:7200/repositories/" + userRepo
        if (requests.head(url).status_code) == 400:
            result1 = queryresult(userRepo, queryAge)
            result = pd.read_csv(StringIO(result1))

            result['Age_Range'] = pd.cut(result['agevalue'], [0, 40, 50, 60, 70, 80, 90],
                                         labels=['0-40', '40-50', '50-60', '60-70', '70-80', '80-90'])
            x = result.groupby(['Age_Range']).count()
            if (x.empty == False):
                fig = px.scatter(x, color_discrete_sequence=px.colors.qualitative.Antique, size='value', color='value')
                fig.update_layout(title_text='Cases per Age_range', title_x=0.5)
                fig.update_traces(hovertemplate='Age_range: %{x} <br>Count: %{y}')
                return fig
            else:
                fig = px.scatter(None)
                return fig
        else:
            fig = px.scatter(None)
            return fig
    else:
        fig = px.scatter(None)
        return fig

@app.callback(
    Output("pie-chart", "figure"),
    [Input("userRepo", "value"),
     Input("columns", "value")])
def generate_chart(userRepo, columns):
    result = pd.DataFrame()
    result_data = ''
    if userRepo:
        url = "http://rdf-store:7200/repositories/" + userRepo
        if (requests.head(url).status_code) == 400:
            if columns == "gender":
                result_data = queryresult(userRepo, queryG)
            elif columns == "tstage":
                result_data = queryresult(userRepo, queryT)
            elif columns == "nstage":
                result_data = queryresult(userRepo, queryN)
            elif columns == "mstage":
                result_data = queryresult(userRepo, queryM)
            elif columns == "survival":
                result_data = queryresult(userRepo, queryS)
            elif columns == "hpv":
                result_data = queryresult(userRepo, queryHpv)
            elif columns == "ajcc":
                result_data = queryresult(userRepo, queryAjcc)
            elif columns == "TumourLocation":
                result_data = queryresult(userRepo, queryTumour)
            elif columns == "therapy":
                result_data = queryresult(userRepo, queryChemo)
            result = pd.read_csv(StringIO(result_data))
            result[columns].replace(codedict, inplace=True)
            # print(result)
            if (result.empty == False):
                fig = px.pie(result, names=result[columns], color_discrete_sequence=px.colors.sequential.RdBu)
                return fig
            else:
                fig = px.pie(None)
                return fig
        else:
            fig = px.pie(None)
            return fig
    else:
        fig = px.pie(None)
        return fig

@app.callback(
    Output("loading-output-2", "children"),
    Input("userRepo", "value"))
def input_triggers_nested(value):
    time.sleep(2)

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
