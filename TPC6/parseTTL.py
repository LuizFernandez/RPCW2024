import json
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL, XSD

# Carregar o grafo RDF existente
g = Graph()
g.parse("Cinema.ttl")

# Definir o namespace do seu grafo RDF
cinema = Namespace('http://rpcw.di.uminho.pt/2024/cinema/')

# Função para formatar URI
def uri_format(individuo):
    return URIRef(f"{cinema}{individuo.replace(" ", "_").replace('"', '').replace("%", "")}")

# Abrir o Ficheiro JSON e ler os dados
with open("Cinema.json", "r") as file:
    db = json.load(file)

# Separar Atores de Filmes
movies = db["movies"]
actors = db["atores"]


# Iterar sobre os atores dentro do Cinema.json
for actor in actors:
    actor_uri = uri_format(actor['nome'])
    g.add((actor_uri, RDF.type, OWL.NamedIndividual))
    g.add((actor_uri, RDF.type, cinema.Actor))
    g.add((actor_uri, cinema.name, Literal(actor['nome'], datatype=XSD.string)))

# Iterar sobre os filmes dentro do Cinema.json
for movie in movies:
    film_uri = uri_format(movie['designacao'])
    g.add((film_uri, RDF.type, OWL.NamedIndividual))
    g.add((film_uri, RDF.type, cinema.Film))
    g.add((film_uri, cinema.title, Literal(movie['designacao'], datatype=XSD.string)))
    g.add((film_uri, cinema.description, Literal(movie["designacao"], datatype=XSD.string)))
    g.add((film_uri, cinema.duration, Literal(movie["duracao"], datatype=XSD.string)))

    for actor in movie['atores']:
        actor_uri = uri_format(actor)
        g.add((film_uri, cinema.hasActor, actor_uri))

    for director in movie['diretor']:
        director_uri = uri_format(director)
        g.add((director_uri, RDF.type, OWL.NamedIndividual))
        g.add((director_uri, RDF.type, cinema.Director))
        g.add((director_uri, cinema.name, Literal(director, datatype=XSD.string)))
        g.add((film_uri, cinema.hasDirector, director_uri))

    for writer in movie['escritores']:
        writer_uri = uri_format(writer)
        g.add((writer_uri, RDF.type, OWL.NamedIndividual))
        g.add((writer_uri, RDF.type, cinema.Writer))
        g.add((writer_uri, cinema.name, Literal(writer, datatype=XSD.string)))
        g.add((film_uri, cinema.hasWriter, writer_uri))

    for musician in movie['musico']:
        musician_uri = uri_format(musician)
        g.add((musician_uri, RDF.type, OWL.NamedIndividual))
        g.add((musician_uri, RDF.type, cinema.Musician))
        g.add((musician_uri, cinema.name, Literal(musician, datatype=XSD.string)))
        g.add((film_uri, cinema.hasMusic, musician_uri))

# Salvar o grafo RDF atualizado
g.serialize(destination="cinema_populated.ttl", format="turtle")