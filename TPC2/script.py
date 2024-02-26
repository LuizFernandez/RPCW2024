import json

def get_instrumento_id(nome, db):
    for data in db:
        if nome == data["nome"]:
            return data["id"]
        
def instrument_classification(nome):
    sopro = ["trombone", "trompa", "trompete", "tuba", "saxofone", "oboé", "fliscorne", "flauta", "fagote", "eufónio", "corne inglês"]
    cordas = ["guitarra", "harpa", "piano", "violoncelo", "violino", "viola de arco", "bandolim", "contrabaixo"]

    nome = nome.lower()

    r = None

    if nome in sopro:
        r = "Sopro"
    elif nome in cordas:
        r = "Cordas"
    else:
        r = "Outros"

def course_classification(id):

    r = None

    if id.startswith("CS"):
        r = "Supletivo"
    else:
        r = "Básico"
    
    return r

def fix_course_id_in_students(student, courses):

    for course in courses:
        if student["instrumento"] == course["instrumento"]:
            if (student["curso"].startswith("CS") and course["id"].startswith("CS")) or (student["curso"].startswith("CB") and course["id"].startswith("CB")):
                if student["curso"] != course["id"]:
                    return course["id"]

        


f = open("db.json", encoding='utf-8')
db = json.load(f)
f.close()

cursos = db["cursos"]
for curso in cursos:
    curso["instrumento"] = curso["instrumento"]["id"]

instrumentos = db["instrumentos"]
for instrumento in instrumentos:
    instrumento["nome"] = instrumento["#text"]
    del(instrumento["#text"])

alunos = db["alunos"]
for aluno in alunos:
    aluno["instrumento"] = get_instrumento_id(aluno["instrumento"], instrumentos)
    aluno["curso"] = fix_course_id_in_students(aluno, cursos)


print("""@prefix : <http://rpcw.di.uminho.pt/2024/musica/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://rpcw.di.uminho.pt/2024/musica/> .

<http://rpcw.di.uminho.pt/2024/musica> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/musica#aprendeInstrumento
:aprendeInstrumento rdf:type owl:ObjectProperty ;
                    rdfs:domain :Aluno ;
                    rdfs:range :Instrumento .


###  http://rpcw.di.uminho.pt/2024/musica#ensinaInstrumento
:ensinaInstrumento rdf:type owl:ObjectProperty ;
                   rdfs:domain :Curso ;
                   rdfs:range :Instrumento .


###  http://rpcw.di.uminho.pt/2024/musica#inscritoEm
:inscritoEm rdf:type owl:ObjectProperty ;
            rdfs:domain :Aluno ;
            rdfs:range :Curso .


#################################################################
#    Data properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/musica#ano_curso
:ano_curso rdf:type owl:DatatypeProperty ;
           rdfs:domain :Aluno .


###  http://rpcw.di.uminho.pt/2024/musica#dataNasc
:dataNasc rdf:type owl:DatatypeProperty ;
          rdfs:domain :Aluno .


###  http://rpcw.di.uminho.pt/2024/musica#designação
:designação rdf:type owl:DatatypeProperty ;
            rdfs:domain :Curso .


###  http://rpcw.di.uminho.pt/2024/musica#duração
:duração rdf:type owl:DatatypeProperty ;
         rdfs:domain :Curso .


###  http://rpcw.di.uminho.pt/2024/musica#id_aluno
:id_aluno rdf:type owl:DatatypeProperty ;
          rdfs:domain :Aluno .


###  http://rpcw.di.uminho.pt/2024/musica#id_curso
:id_curso rdf:type owl:DatatypeProperty ;
          rdfs:domain :Curso .


###  http://rpcw.di.uminho.pt/2024/musica#id_instrumento
:id_instrumento rdf:type owl:DatatypeProperty ;
                rdfs:domain :Instrumento .


###  http://rpcw.di.uminho.pt/2024/musica#instrumento
:instrumento rdf:type owl:DatatypeProperty ;
             rdfs:domain :Instrumento .


###  http://rpcw.di.uminho.pt/2024/musica#nome
:nome rdf:type owl:DatatypeProperty ;
      rdfs:domain :Aluno .


#################################################################
#    Classes
#################################################################

###  http://rpcw.di.uminho.pt/2024/musica#Aluno
:Aluno rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/musica#Básico
:Básico rdf:type owl:Class ;
        rdfs:subClassOf :Curso ;
        owl:disjointWith :Supletivo .


###  http://rpcw.di.uminho.pt/2024/musica#Cordas
:Cordas rdf:type owl:Class ;
        rdfs:subClassOf :Tipo .


###  http://rpcw.di.uminho.pt/2024/musica#Curso
:Curso rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/musica#Instrumento
:Instrumento rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/musica#Outros
:Outros rdf:type owl:Class ;
        rdfs:subClassOf :Tipo .


###  http://rpcw.di.uminho.pt/2024/musica#Sopro
:Sopro rdf:type owl:Class ;
       rdfs:subClassOf :Tipo .


###  http://rpcw.di.uminho.pt/2024/musica#Supletivo
:Supletivo rdf:type owl:Class ;
           rdfs:subClassOf :Curso .


###  http://rpcw.di.uminho.pt/2024/musica#Tipo
:Tipo rdf:type owl:Class ;
      rdfs:subClassOf :Instrumento .


#################################################################
#    Individuals
#################################################################
""")

for aluno in alunos:
    al = f"""
###  http://rpcw.di.uminho.pt/2024/musica#{aluno["id"]}
:{aluno["id"]} rdf:type owl:NamedIndividual ,
                :Aluno ;
       :aprendeInstrumento :{aluno["instrumento"]} ;
       :inscritoEm :{aluno["curso"]} ;
       :ano_curso "{aluno["anoCurso"]}" ;
       :dataNasc "{aluno["dataNasc"]}" ;
       :id_aluno "{aluno["id"]}" ;
       :nome "{aluno["nome"].replace(" ", "_")}" .
"""
    print(al)

for curso in cursos:
    cur = f"""
###  http://rpcw.di.uminho.pt/2024/musica#{curso["id"]}
:{curso["id"]} rdf:type owl:NamedIndividual ,
              :{course_classification(curso["id"])} ;
     :ensinaInstrumento :{curso["instrumento"]} ;
     :designação "{curso["designacao"].replace(" ", "_")}" ;
     :duração "{curso["duracao"]}" ;
     :id_curso "{curso["id"]}" .
"""
    print(cur)

for instrumento in instrumentos:
    inst = f"""
###  http://rpcw.di.uminho.pt/2024/musica#{instrumento["id"]}
:{instrumento["id"]} rdf:type owl:NamedIndividual ,
             :{instrument_classification(instrumento["nome"])} ;
    :id_instrumento "{instrumento["id"]}" ;
    :instrumento "{instrumento["nome"].replace(" ", "_")}" .
"""
    print(inst)


print("""
#################################################################
#    General axioms
#################################################################

[ rdf:type owl:AllDisjointClasses ;
  owl:members ( :Cordas
                :Outros
                :Sopro
              )
] .


###  Generated by the OWL API (version 4.5.26.2023-07-17T20:34:13Z) https://github.com/owlcs/owlapi""")