import json

f = open("mapa-virtual.json")
db = json.load(f)
f.close()

cidades = db["cidades"]
ligacoes = db["ligacoes"]

print("""@prefix : <http://rpcw.di.uminho.pt/2024/mapa_virtual/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://rpcw.di.uminho.pt/2024/mapa_virtual/> .

<http://rpcw.di.uminho.pt/2024/mapa_virtual> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/mapa_virtual#temDestino
:temDestino rdf:type owl:ObjectProperty ;
            rdfs:domain :Ligação ;
            rdfs:range :Cidade ;
            owl:propertyDisjointWith :temOrigem .


###  http://rpcw.di.uminho.pt/2024/mapa_virtual#temOrigem
:temOrigem rdf:type owl:ObjectProperty ;
           rdfs:domain :Ligação ;
           rdfs:range :Cidade .


#################################################################
#    Data properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/mapa_virtual#descrição
:descrição rdf:type owl:DatatypeProperty ;
           rdfs:domain :Cidade .


###  http://rpcw.di.uminho.pt/2024/mapa_virtual#distrito
:distrito rdf:type owl:DatatypeProperty ;
          rdfs:domain :Cidade .


###  http://rpcw.di.uminho.pt/2024/mapa_virtual#distância
:distância rdf:type owl:DatatypeProperty ;
           rdfs:domain :Ligação .


###  http://rpcw.di.uminho.pt/2024/mapa_virtual#id_cidade
:id_cidade rdf:type owl:DatatypeProperty ;
           rdfs:domain :Cidade .


###  http://rpcw.di.uminho.pt/2024/mapa_virtual#id_ligação
:id_ligação rdf:type owl:DatatypeProperty ;
            rdfs:domain :Ligação .


###  http://rpcw.di.uminho.pt/2024/mapa_virtual#nome
:nome rdf:type owl:DatatypeProperty ;
      rdfs:domain :Cidade .


###  http://rpcw.di.uminho.pt/2024/mapa_virtual#população
:população rdf:type owl:DatatypeProperty ;
           rdfs:domain :Cidade .


#################################################################
#    Classes
#################################################################

###  http://rpcw.di.uminho.pt/2024/mapa_virtual#Cidade
:Cidade rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/mapa_virtual#Ligação
:Ligação rdf:type owl:Class .


#################################################################
#    Individuals
#################################################################

""")

for cidade in cidades:
    print(f"""###  http://rpcw.di.uminho.pt/2024/mapa_virtual#{cidade["id"]}
:{cidade["id"]} rdf:type owl:NamedIndividual ,
              :Cidade ;
     :descrição "{cidade["descrição"]}" ;
     :distrito "{cidade["distrito"]}" ;
     :id_cidade "{cidade["id"]}" ;
     :nome "{cidade["nome"]}" ;
     :população "{cidade["população"]}"^^xsd:int .

""")
    
for ligacao in ligacoes:
    print(f"""###  http://rpcw.di.uminho.pt/2024/mapa_virtual#{ligacao["id"]}
:{ligacao["id"]} rdf:type owl:NamedIndividual ,
             :Ligação ;
    :temDestino :{ligacao["destino"]} ;
    :temOrigem :{ligacao["origem"]} ;
    :distância "{ligacao["distância"]}" ;
    :id_ligação "{ligacao["id"]}" .
""")
    

print("""###  Generated by the OWL API (version 4.5.26.2023-07-17T20:34:13Z) https://github.com/owlcs/owlapi""")