import requests
import json

# Function to fecth data
def fecthFromDBpedia(params, db):
    # Define the DBpedia SPARQL endpoint
    sparql_endpoint = "http://dbpedia.org/sparql"

    # Define the headers
    headers = {
        "Accept": "application/sparql-results+json"
    }

    # Send the SPARQL query using requests
    response = requests.get(sparql_endpoint, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        results = response.json()
        # Print the results
        #for result in results["results"]["bindings"]:
        for result in results["results"]["bindings"]:
            actor_uri = result["actor"]["value"]
            actor_name = result["name"]["value"]
            actor_films = list(set(result["filmList"]["value"].split(",")))
            actor = {"uri": actor_uri, "nome": actor_name, "filmes": actor_films}
            db["atores"].append(actor)
    else:
        print("Error:", response.status_code)
        print(response.text)
        return None
    
    return db

f = open("movies.json", "r")
db = json.loads(f.read())
f.close()

new_db = {}
new_db["movies"] = db
new_db["atores"] = []

sparql_query_actors = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>

SELECT DISTINCT ?actor ?name (GROUP_CONCAT(?filmName; SEPARATOR=";") AS ?filmList) WHERE {{
    ?actor rdf:type yago:Actor109765278;
           rdfs:label ?name.
    
    OPTIONAL {{
        ?film dbo:starring ?actor.
        ?film rdfs:label ?filmName.
        FILTER (lang(?filmName) = "en")
    }}
    FILTER (lang(?name) = "en")
}}GROUP BY ?actor ?name
"""

sparql_query_actress = """

PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>

SELECT DISTINCT ?actor ?name (GROUP_CONCAT(?filmName; SEPARATOR=",") AS ?filmList) WHERE {{
    ?actor rdf:type yago:Actress109767700;
           rdfs:label ?name.
    
    OPTIONAL {{
        ?film dbo:starring ?actor.
        ?film rdfs:label ?filmName.
        FILTER (lang(?filmName) = "en")
    }}
    FILTER (lang(?name) = "en")
}}GROUP BY ?actor ?name
"""

# Define the parameters
paramsActor = {
    "query": sparql_query_actors,
    "format": "json"
}

new_db = fecthFromDBpedia(paramsActor, new_db)

paramsActress = {
    "query": sparql_query_actress,
    "format": "json"
}

new_db = fecthFromDBpedia(paramsActress, new_db)
if new_db:
    print(new_db)




