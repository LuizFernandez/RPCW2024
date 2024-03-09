
from  flask import Flask, render_template, url_for
from datetime import datetime

import requests

app = Flask(__name__)

# Data do sistema no formato ISO
data_hora_atual = datetime.now()
data_iso_formatada = data_hora_atual.strftime("%Y-%m-%dT%H:%M:%S")

# GraphDb endPoint
graphdb_endpoint = "http://localhost:7200/repositories/tab_periodica"

@app.route('/')
def index():
    return render_template('index.html', data = {"data": data_iso_formatada})

@app.route('/elementos')
def elementos():
    sparql_query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>                       
PREFIX : <http://www.daml.org/2003/01/periodictable/PeriodicTable#>                                    
                                                                                 
SELECT ?simb ?name ?numb ?group WHERE {                                                
    ?el rdf:type :Element;                                                      
           :atomicNumber ?numb;                                                  
           :name ?name;                                                          
           :symbol ?simb;
           :group ?g.   
    OPTIONAL {?g :number ?group.}
    OPTIONAL {?g :name ?group.}                                                          
}  ORDER BY ?numb   
"""
    resposta = requests.get(graphdb_endpoint,
                            params={"query" : sparql_query},
                            headers={"Accept": 'application/sparql-results+json'})
    
    if resposta.status_code == 200:
        dados = resposta.json()["results"]["bindings"]
        return render_template('elements.html', data = {"data" : dados, "tempo": data_iso_formatada})
    else:
        return render_template('empty.html', data = {"data": data_iso_formatada})

def setState(dados):
    dados[0]['state']['value'] = dados[0]['state']['value'].split('#')[1]

def setClass(dados):
    dados[0]['class']['value'] = dados[0]['class']['value'].split('#')[1]


@app.route('/elementos/<int:number>')
def elemento(number):
    sparql_query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>                       
PREFIX : <http://www.daml.org/2003/01/periodictable/PeriodicTable#>                                    
                                                                                 
SELECT ?simb ?name ?weight ?class ?state ?color ?group WHERE {{                                                                                                     
    ?el    :atomicNumber {number};                                                  
           :name ?name;                                                          
           :symbol ?simb;
           :atomicWeight ?weight;
           :classification ?class;
           :standardState ?state;
           :color ?color;   
           :group ?g.

    OPTIONAL {{?g :number ?group.}}
    OPTIONAL {{?g :name ?group.}}
                                                             
}}   
"""
    resposta = requests.get(graphdb_endpoint,
                            params={"query" : sparql_query},
                            headers={"Accept": 'application/sparql-results+json'})
    
    if resposta.status_code == 200:
        dados = resposta.json()["results"]["bindings"]
        dados[0]["number"] = {"type" : "literal", "value" : "1"}
        setState(dados)
        setClass(dados)
        return render_template('element.html', data = {"data" : dados, "tempo": data_iso_formatada})
    else:
        return render_template('empty.html', data = {"data": data_iso_formatada})

def treat_groups_data(data):

    for value in data:
        if "name" not in value.keys():
            value["name"] = {'type': 'literal', 'value': ''}
        elif "number" not in value.keys():
            value["number"] = {'datatype': 'http://www.w3.org/2001/XMLSchema#integer', 'type': 'literal', 'value': ''}

@app.route("/grupos")
def grupos():
    sparql_query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>                       
PREFIX : <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
                                                                                 
SELECT ?number ?name WHERE {                                                      
	 ?g rdf:type :Group.                                                          
   OPTIONAL {?g :name ?name.}                                                   
   OPTIONAL {?g :number ?number}                                                
}      
"""
    resposta = requests.get(graphdb_endpoint,
                            params={"query" : sparql_query},
                            headers={"Accept": 'application/sparql-results+json'})
    
    if resposta.status_code == 200:
        dados = resposta.json()["results"]["bindings"]
        treat_groups_data(dados)
        return render_template('groups.html', data = {"data" : dados, "tempo": data_iso_formatada})
    else:
        return render_template('empty.html', data = {"data": data_iso_formatada})

def render_elements(dados):
    
    elements = []

    for value in dados:
        if "element" in value.keys():
            elements.append(value["element"]["value"])

    return {"type": "literal", "value": elements}

@app.route('/grupos/<string:grupo>')
def grupo(grupo):
    flag = False
    value = f"OPTIONAL {{?g :number {grupo}}}" 

    try:
        int(grupo)
    except ValueError:
        value = f"OPTIONAL {{?g :name {grupo}.}}"
        flag = True

    sparql_query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>                       
PREFIX : <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
                                                                                 
SELECT ?element WHERE {{                                                      
	 ?g rdf:type :Group.                                                          
     {value}                                                   
     ?g :element ?el.
     ?el :symbol ?element.                   
}}      
"""
    resposta = requests.get(graphdb_endpoint,
                            params={"query" : sparql_query},
                            headers={"Accept": 'application/sparql-results+json'})
    
    if resposta.status_code == 200:
        dados = resposta.json()["results"]["bindings"]
        data = {}
        if flag:
            data["name"] = {"type" : "literal", "value" : f"{grupo}"}
            data["number"] = {"type" : "literal", "value" : ""}
        else:
            data["name"] = {"type" : "literal", "value" : ""}
            data["number"] = {"type" : "literal", "value" : f"{grupo}"}
        elemtens = render_elements(dados)
        data["elements"] = elemtens
        print(data)
        return render_template('group.html', data = {"data" : data, "tempo": data_iso_formatada})
    else:
        return render_template('empty.html', data = {"data": data_iso_formatada})

if __name__ == "__main__":
    app.run(debug=True)