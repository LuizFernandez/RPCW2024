import json
from icecream import ic

with open("aval-alunos.json") as file:
    content = json.loads(file.read())

cursos = {}
testes = []
alunos = []
tpcs = []

for a in content["alunos"]:
    if a["curso"] not in cursos.keys():
        cursos[a["curso"]] = []
    cursos[a["curso"]].append(a["idAluno"])

    tempA = {
        "curso": a["curso"],
        "nome": a["nome"],
        "id_aluno": a["idAluno"],
        "nota_projeto": a["projeto"],
        "exames": [],
        "tpcs": []
    } 

    for e in a["exames"]:
        value = a["exames"][e]
        tempE = {}
        match(e):
            case "recurso":
                tempE["id_exame"] = f"{a['idAluno']}_Recurso"
                tempE["type"] = "Recurso"
            case "especial":
                tempE["id_exame"] = f"{a['idAluno']}_Especial"
                tempE["type"] = "Especial"
            case "normal":
                tempE["id_exame"] = f"{a['idAluno']}_Normal"
                tempE["type"] = "Normal"
        tempE["exame_nota"] = value
        tempE["aluno"] = a['idAluno']
        testes.append(tempE)
        tempA["exames"].append(tempE["id_exame"])

    for tpc in a["tpc"]:
        tempT = {}
        match(tpc["tp"]):
            case "tpc1":
                tempT["id_tpc"] = f"{a['idAluno']}_TPC1"
            case "tpc2":
                tempT["id_tpc"] = f"{a['idAluno']}_TPC2"
            case "tpc3":
                tempT["id_tpc"] = f"{a['idAluno']}_TPC3"
            case "tpc4":
                tempT["id_tpc"] = f"{a['idAluno']}_TPC4"
            case "tpc5":
                tempT["id_tpc"] = f"{a['idAluno']}_TPC5"
            case "tpc6":
                tempT["id_tpc"] = f"{a['idAluno']}_TPC6"
            case "tpc7":
                tempT["id_tpc"] = f"{a['idAluno']}_TPC7"
            case "tpc8":
                tempT["id_tpc"] = f"{a['idAluno']}_TPC8"
        tempT["tpc_nota"] = tpc["nota"]
        tempT["aluno"] = a['idAluno']
        tpcs.append(tempT)
        tempA["tpcs"].append(tempT["id_tpc"])

    alunos.append(tempA)


ttl = """@prefix : <http://rpcw.di.uminho.pt/2024/alunos/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://rpcw.di.uminho.pt/2024/alunos/> .

<http://rpcw.di.uminho.pt/2024/alunos> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/alunos#exameRealizadoPor
:exameRealizadoPor rdf:type owl:ObjectProperty ;
                   owl:inverseOf :realizouExame .


###  http://rpcw.di.uminho.pt/2024/alunos#inscritoEm
:inscritoEm rdf:type owl:ObjectProperty ;
            owl:inverseOf :temInscritos ;
            rdfs:domain :Aluno ;
            rdfs:range :Curso .


###  http://rpcw.di.uminho.pt/2024/alunos#realiazouTPC
:realiazouTPC rdf:type owl:ObjectProperty ;
              owl:inverseOf :tpcRealizadoPor ;
              rdfs:domain :Aluno ;
              rdfs:range :TPC .


###  http://rpcw.di.uminho.pt/2024/alunos#realizouExame
:realizouExame rdf:type owl:ObjectProperty ;
               rdfs:domain :Aluno ;
               rdfs:range :Exame .


###  http://rpcw.di.uminho.pt/2024/alunos#temInscritos
:temInscritos rdf:type owl:ObjectProperty .


###  http://rpcw.di.uminho.pt/2024/alunos#tpcRealizadoPor
:tpcRealizadoPor rdf:type owl:ObjectProperty .


#################################################################
#    Data properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/alunos#curso
:curso rdf:type owl:DatatypeProperty ;
       rdfs:domain :Curso .


###  http://rpcw.di.uminho.pt/2024/alunos#exame_nota
:exame_nota rdf:type owl:DatatypeProperty ;
            rdfs:domain :Exame .


###  http://rpcw.di.uminho.pt/2024/alunos#id_aluno
:id_aluno rdf:type owl:DatatypeProperty ;
          rdfs:domain :Aluno .


###  http://rpcw.di.uminho.pt/2024/alunos#id_exame
:id_exame rdf:type owl:DatatypeProperty ;
          rdfs:domain :Exame .


###  http://rpcw.di.uminho.pt/2024/alunos#id_tpc
:id_tpc rdf:type owl:DatatypeProperty ;
        rdfs:subPropertyOf owl:topDataProperty .


###  http://rpcw.di.uminho.pt/2024/alunos#name
:name rdf:type owl:DatatypeProperty ;
      rdfs:domain :Aluno .


###  http://rpcw.di.uminho.pt/2024/alunos#nota_projeto
:nota_projeto rdf:type owl:DatatypeProperty ;
              rdfs:domain :Aluno .


###  http://rpcw.di.uminho.pt/2024/alunos#tpc_nota
:tpc_nota rdf:type owl:DatatypeProperty ;
          rdfs:domain :TPC .


###  http://rpcw.di.uminho.pt/2024/alunos#tpc_number
:tpc_number rdf:type owl:DatatypeProperty ;
            rdfs:domain :TPC .


#################################################################
#    Classes
#################################################################

###  http://rpcw.di.uminho.pt/2024/alunos#Aluno
:Aluno rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/alunos#Curso
:Curso rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/alunos#Especial
:Especial rdf:type owl:Class ;
          rdfs:subClassOf :Exame .


###  http://rpcw.di.uminho.pt/2024/alunos#Exame
:Exame rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/alunos#Normal
:Normal rdf:type owl:Class ;
        rdfs:subClassOf :Exame .


###  http://rpcw.di.uminho.pt/2024/alunos#Recurso
:Recurso rdf:type owl:Class ;
         rdfs:subClassOf :Exame .


###  http://rpcw.di.uminho.pt/2024/alunos#TPC
:TPC rdf:type owl:Class .


#################################################################
#    Individuals
#################################################################
"""

for a in alunos:

    tpc_aluno = ""
    for tpc in range(0,len(a["tpcs"]) - 1):
        tpc_aluno += f":{a['tpcs'][tpc]} ,\n"

    tpc_aluno += f":{a['tpcs'][len(a['tpcs']) - 1]} ;\n"

    exame_aluno = ""
    for exame in range(0,len(a["exames"]) - 1):
        exame_aluno += f":{a['exames'][exame]} ,\n"

    exame_aluno += f":{a['exames'][len(a['exames']) - 1]} ;\n"

    ttl_alunos = f"""###  http://rpcw.di.uminho.pt/2024/alunos#{a["id_aluno"]}
:{a["id_aluno"]} rdf:type owl:NamedIndividual ,
                 :Aluno ;
        :inscritoEm :{a["curso"]} ;
        :realiazouTPC {tpc_aluno}
        :realizouExame {exame_aluno}
        :id_aluno "{a["id_aluno"]}" ;
        :name "{a["nome"]}" ;
        :nota_projeto {a["nota_projeto"]} .

        """
    
    ttl += ttl_alunos


for t in testes:
    
    ttl_exame = f"""###  http://rpcw.di.uminho.pt/2024/alunos#{t["id_exame"]}
:{t["id_exame"]} rdf:type owl:NamedIndividual ,
                          :{t["type"]} ;
                 :exameRealizadoPor :{t["aluno"]} ;
                 :exame_nota {int(t['exame_nota'])} ;
                 :id_exame "{t["id_exame"]}" .
"""
    
    ttl += ttl_exame

for t in tpcs:

    ttl_tpc = f"""###  http://rpcw.di.uminho.pt/2024/alunos#{t["id_tpc"]}
:{t["id_tpc"]} rdf:type owl:NamedIndividual ,
                      :TPC ;
             :tpcRealizadoPor :{t["aluno"]} ;
             :id_tpc "{t["id_tpc"]}" ;
             :tpc_nota {t["tpc_nota"]} .
             """
    
    ttl += ttl_tpc

for key in cursos:
    value = cursos[key]

    inscrito_aluno = ""
    for a in range(0,len(value) - 1):
        inscrito_aluno += f":{value[a]} ,\n"

    inscrito_aluno += f":{value[len(value) - 1]} ;\n"


    ttl_curso = f"""###  http://rpcw.di.uminho.pt/2024/alunos#{key}
:{key} rdf:type owl:NamedIndividual ,
              :Curso ;
     :temInscritos {inscrito_aluno}
     :curso "{key}" .
"""
    
    ttl += ttl_curso

print(ttl)