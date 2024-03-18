import requests
import json

# Define the DBpedia SPARQL endpoint
sparql_endpoint = "http://dbpedia.org/sparql"

# Define the SPARQL query
sparql_query = """

PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?film ?filmName ?time (GROUP_CONCAT(?actorName; SEPARATOR=";") AS ?actorList) (GROUP_CONCAT(?writerName; SEPARATOR=",") AS ?writerList) (GROUP_CONCAT(?directorName; SEPARATOR=",") AS ?directorList) (GROUP_CONCAT(?musicianName; SEPARATOR=",") AS ?musicianList) WHERE {{
    ?film a dbo:Film;
          rdfs:label ?filmName;
          dbo:runtime ?time.
    
    OPTIONAL {{
        ?film dbo:starring ?actor.
        ?actor rdfs:label ?actorName.
        FILTER (lang(?actorName) = "en")
    }}

    OPTIONAL {{ 
        ?film dbo:director ?director .
        ?director rdfs:label ?directorName .
        FILTER (lang(?directorName) = "en")
    }}

    OPTIONAL {{ 
        ?film dbo:writer ?writer .
        ?writer rdfs:label ?writerName .
        FILTER (lang(?writerName) = "en")
    }}

    OPTIONAL {{ 
        ?film dbo:musicComposer ?musician .
        ?musician rdfs:label ?musicianName .
        FILTER (lang(?musicianName) = "en")
    }}

    FILTER (lang(?filmName) = "en")
}} GROUP BY ?film ?time ?filmName
"""

# Define the headers
headers = {
    "Accept": "application/sparql-results+json"
}

# Define the parameters
params = {
    "query": sparql_query,
    "format": "json"
}

# Send the SPARQL query using requests
response = requests.get(sparql_endpoint, params=params, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    results = response.json()
    db = []
    # Print the results
    for result in results["results"]["bindings"]:
        movie_uri = result["film"]["value"]
        movie_name = result["filmName"]["value"]
        movie_time = result["time"]["value"]
        movie_actors = list(set(result["actorList"]["value"].split(",")))
        movie_writers = list(set(result["writerList"]["value"].split(",")))
        movie_directors = list(set(result["directorList"]["value"].split(",")))
        movie_musician = list(set(result["musicianList"]["value"].split(",")))
        movie = {"uri": movie_uri, "designacao": movie_name, "duracao": movie_time, "atores": movie_actors, "escritores": movie_writers, "diretor": movie_directors, "musico": movie_musician}
        db.append(movie)
    print(json.dumps(db))
else:
    print("Error:", response.status_code)
    print(response.text)
