from flask import Flask, jsonify, request
from SPARQLWrapper import SPARQLWrapper, JSON
import requests

from icecream import ic

app = Flask(__name__)

# Endpoint do GraphDB
graphdb_endpoint = "http://localhost:7200/repositories/aval-alunos"


# Devolve a lista dos alunos, ordenada alfabeticamente por nome, com os campos: idAluno, nome e curso;
def treat_alunos(data):

    treated_data = []

    for d in data:
        value = {}
        for key in d.keys():
            value[key] = d[key]["value"]
        treated_data.append(value)

    return treated_data

@app.route("/api/alunos", methods=["GET"])
def alunos():
    curso = request.args.get('curso')
    groupBy = request.args.get('groupBy')

    if curso is not None:
        return alunos_curso(curso)
    elif groupBy is not None:
        match(groupBy):
            case "curso":
                return groupByCurso()
            case "projeto":
                return groupByProjeto()
            case "recurso":
                return groupByRecurso()
            case _:
                return {"error": "Key used to group values is invalid!"}
    else:
        sparql_query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/alunos/>
SELECT ?id ?nome ?curso WHERE { 
	?s rdf:type :Aluno;
       :name ?nome;
       :id_aluno ?id;
       :inscritoEm ?c.
    ?c :curso ?curso
} ORDER BY ?nome
"""

        response = requests.get(graphdb_endpoint,
                            params={"query": sparql_query},
                            headers={'Accept': 'application/sparql-results+json'})

        if response.status_code == 200:
            alunos_data = response.json()['results']['bindings']
            data = treat_alunos(alunos_data)
            return data
        else:
            return {"Error": "DataBase is probably down!!"}


def treat_aluno(data):

    aluno = {}

    aluno["exame"] = []

    for d in data:
        for key in d.keys():
            if key not in aluno.keys():
                if key != "exame" and key != "nota":
                    aluno[key] = d[key]["value"]
        
        aluno["exame"].append((d["exame"]["value"].split("/")[-1], d["nota"]["value"]))

    return aluno

# Devolve a informação completa de um aluno (nesta rota, considere para id o campo idAluno);
@app.route("/api/alunos/:<id>", methods=["GET"])
def aluno(id):
    sparql_query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/alunos/>
SELECT ?nome ?curso ?projeto ?exame ?nota (SUM(?tpcs) as ?nota_tpc) WHERE {{
	?s rdf:type :Aluno;
       :name ?nome;
       :id_aluno "{id}";
       :inscritoEm ?c;
       :nota_projeto ?projeto;
       :realiazouTPC ?tpc;
       :realizouExame ?e.

    ?c :curso ?curso.
    
    ?e rdf:type ?exame;
       :exame_nota ?nota.
    
    ?tpc :tpc_nota ?tpcs
    
    FILTER (?exame in (:Especial, :Normal, :Recurso))

}}
GROUP BY ?nome ?curso ?projeto ?exame ?nota
ORDER BY ?nome
"""

    response = requests.get(graphdb_endpoint,
                            params={"query": sparql_query},
                            headers={'Accept': 'application/sparql-results+json'})

    if response.status_code == 200:
        aluno_data = response.json()['results']['bindings']
        data = treat_aluno(aluno_data)
        data["idAluno"] = id
        return data
    else:
        return {"Error": "DataBase is probably down!!"}

def treat_alunos_curso(data):

    curso = {"alunos": []}

    for d in data:
        curso["alunos"].append(d["nome"]["value"])

    return curso

# /api/alunos?curso="X"
def alunos_curso(curso):
    sparql_query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/alunos/>
SELECT ?nome WHERE {{
	?s rdf:type :Curso;
       :curso "{curso}";
       :temInscritos ?a.
    
    ?a :name ?nome
}}ORDER BY ?nome
"""
    response = requests.get(graphdb_endpoint,
                            params={"query": sparql_query},
                            headers={'Accept': 'application/sparql-results+json'})

    if response.status_code == 200:
        curso_data = response.json()['results']['bindings']
        data = treat_alunos_curso(curso_data)
        data["curso"] = curso
        return data
    else:
        return {"Error": "DataBase is probably down!!"}

@app.route("/api/alunos/tpc", methods=["GET"])
def tpcs():
    sparql_query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/alunos/>
SELECT ?id ?nome ?curso (COUNT(?tpc) as ?ntpcs) WHERE {{
	?s rdf:type :Aluno;
       :realiazouTPC ?tpc;
       :name ?nome;
       :id_aluno ?id;
       :inscritoEm ?c.
    
   	?c :curso ?curso.
}}
GROUP BY ?id ?nome ?curso
ORDER BY ?nome
"""
    response = requests.get(graphdb_endpoint,
                            params={"query": sparql_query},
                            headers={'Accept': 'application/sparql-results+json'})

    if response.status_code == 200:
        curso_data = response.json()['results']['bindings']
        data = treat_alunos(curso_data)
        return data
    else:
        return {"Error": "DataBase is probably down!!"}
    
# /api/alunos?groupBy=curso
def groupByCurso():
    sparql_query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/alunos/>
SELECT ?c (COUNT(?a) as ?nalunos) WHERE {{
	?s rdf:type :Curso;
       :curso ?c;
       :temInscritos ?a.
}}GROUP BY ?c
"""
    response = requests.get(graphdb_endpoint,
                            params={"query": sparql_query},
                            headers={'Accept': 'application/sparql-results+json'})

    if response.status_code == 200:
        curso_data = response.json()['results']['bindings']
        data = treat_alunos(curso_data)
        return data
    else:
        return {"Error": "DataBase is probably down!!"}

# /api/alunos?groupBy=projeto   
def groupByProjeto():
    sparql_query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/alunos/>
SELECT ?nota (COUNT(?s) as ?nalunos) WHERE {{
	?s rdf:type :Aluno;
       :nota_projeto ?nota;
}}GROUP BY ?nota
"""
    response = requests.get(graphdb_endpoint,
                            params={"query": sparql_query},
                            headers={'Accept': 'application/sparql-results+json'})

    if response.status_code == 200:
        curso_data = response.json()['results']['bindings']
        data = treat_alunos(curso_data)
        return data
    else:
        return {"Error": "DataBase is probably down!!"}

# /api/alunos?groupBy=recurso  
def groupByRecurso():
    sparql_query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/alunos/>
SELECT ?id ?nome ?curso ?nota WHERE {{
	?s rdf:type :Aluno;
       :name ?nome;
       :id_aluno ?id;
       :inscritoEm ?c;
       :realizouExame ?e.
    
    ?c :curso ?curso.
    
    ?e rdf:type :Recurso;
       :exame_nota ?nota.
}}ORDER BY ?nome
"""
    response = requests.get(graphdb_endpoint,
                            params={"query": sparql_query},
                            headers={'Accept': 'application/sparql-results+json'})

    if response.status_code == 200:
        curso_data = response.json()['results']['bindings']
        data = treat_alunos(curso_data)
        return data
    else:
        return {"Error": "DataBase is probably down!!"}
    
def getNota(d):

    nota_final = 0
    
    if d["projeto"] < 10:
        nota_final = "R"
    else:
        nota_exame = "R"
        for e in ["Normal", "Recurso", "Especial"]:
            if e in d["exames"].keys():
                if d["exames"][e] < 10:
                    nota_exame = "R"
                else:
                    nota_exame = d["exames"][e]
            
        if type(nota_exame) is not str:
            nota_final = d["tpc"]
            nota_final += d["projeto"] * 0.4
            nota_final += nota_exame * 0.4
            if nota_final < 10:
                nota_final = "R"
        else:
            nota_final = nota_exame

    return nota_final

def alunos_nota_final(data):


    notas = []

    i = 0
    for d in data:
        id = d["id"]["value"]
        if len(notas) == 0:
            notas.append({
                "id": id,
                "nome": d["nome"]["value"],
                "curso": d["curso"]["value"],
                "nota_final": "",
                "exames": {},
                "tpc": float(d["nota_tpc"]["value"]),
                "projeto": float(d["projeto"]["value"])
            })
        elif id != notas[i]["id"]:
            notas.append({
                "id": id,
                "nome": d["nome"]["value"],
                "curso": d["curso"]["value"],
                "nota_final": "",
                "exames": {},
                "tpc": float(d["nota_tpc"]["value"]),
                "projeto": float(d["projeto"]["value"])
            })
            i += 1
            
            
        notas[i]["exames"][d["exame"]["value"].split("/")[-1]] = float(d["nota"]["value"])

    ic(notas[2])
    for a in notas:
        nota = getNota(a)
        a["nota_final"] = nota
        a.pop("exames", None)
        a.pop("tpc", None)
        a.pop("projeto", None)

    return notas

@app.route("/api/alunos/avaliados")
def avaliados():
    sparql_query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/alunos/>
SELECT ?id ?nome ?curso ?projeto ?exame ?nota (SUM(?tpcs) as ?nota_tpc) WHERE {{
	?s rdf:type :Aluno;
       :name ?nome;
       :id_aluno ?id;
       :inscritoEm ?c;
       :nota_projeto ?projeto;
       :realiazouTPC ?tpc;
       :realizouExame ?e.

    ?c :curso ?curso.
    
    ?e rdf:type ?exame;
       :exame_nota ?nota.
    
    ?tpc :tpc_nota ?tpcs
    
    FILTER (?exame in (:Especial, :Normal, :Recurso))

}}
GROUP BY ?id ?nome ?curso ?projeto ?exame ?nota
ORDER BY ?nome
"""
    response = requests.get(graphdb_endpoint,
                            params={"query": sparql_query},
                            headers={'Accept': 'application/sparql-results+json'})

    if response.status_code == 200:
        curso_data = response.json()['results']['bindings']
        data = alunos_nota_final(curso_data)
        return data
    else:
        return {"Error": "DataBase is probably down!!"}

if __name__ == "__main__":
    app.run(debug=True)