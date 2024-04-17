from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL, XSD
import xml.etree.ElementTree as ET

def import_xml2data(xml):

    data = []

    tree = ET.parse(xml)
    root = tree.getroot()
    i = 0
    for entrada in root.iter('person'): # Vê todos os niveis
        p = {}
        p["id"] = entrada.find('id').text
        p["nome"] = entrada.find('name').text

        for pai in entrada.iter('parent'):
            parent_id = pai.get('ref')
            parent = root.find(f'.//person[id="{parent_id}"]')
            parent_sex = parent.find('sex').text

            if parent_sex == 'F':
                p["mae"] = parent_id
            elif parent_sex == 'M':
                p["pai"] = parent_id
            else:
                print('OUTLIER')
                exit()

        data.append(p)

    return data

def import_data2ttl(turtle, data):

    g = Graph()
    g.parse(turtle)

    for person in data:
        familia = Namespace('http://rpcw.di.uminho.pt/2024/familia/')
        g.add((URIRef(f"{familia}{person['id']}"), RDF.type, OWL.NamedIndividual))
        g.add((URIRef(f"{familia}{person['id']}"), RDF.type, familia.Pessoa))
        g.add((URIRef(f"{familia}{person['id']}"), familia.nome, Literal(person["nome"], datatype=XSD.string)))
        if "mae" in person.keys():
            g.add((URIRef(f"{familia}{person['id']}"), familia.temMae, familia[person["mae"]]))
        if "pai" in person.keys():
            g.add((URIRef(f"{familia}{person['id']}"), familia.temPai, familia[person["pai"]]))

    g.serialize(destination=turtle, format="turtle")

turtleFiles = ["royal.ttl", "biblia.ttl"]
xmlFiles = ["royal.xml", "biblia.xml"]

for i in range(0,len(turtleFiles)):
    import_data2ttl(turtleFiles[i],import_xml2data(xmlFiles[i]))
