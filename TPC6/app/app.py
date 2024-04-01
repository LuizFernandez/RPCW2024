
from  flask import Flask, render_template, url_for
from datetime import datetime

import requests

app = Flask(__name__)

# Data do sistema no formato ISO
data_hora_atual = datetime.now()
data_iso_formatada = data_hora_atual.strftime("%Y-%m-%dT%H:%M:%S")

# GraphDb endPoint
graphdb_endpoint = "http://epl.di.uminho.pt:7200/repositories/cinema2024"

@app.route('/')
def index():
    return render_template('index.html', data={"data": data_iso_formatada})

@app.route('/movies')
def movies():
    sparql_query = """
    PREFIX cinema: <http://rpcw.di.uminho.pt/2024/cinema/>
    SELECT ?title ?release_date ?duration ?director_name WHERE {
        ?film a cinema:Film ;
            cinema:title ?title ;
            cinema:releaseDate ?release_date ;
            cinema:duration ?duration ;
            cinema:hasDirector ?director .
        ?director cinema:name ?director_name .
    }
    """

    response = requests.get(graphdb_endpoint,
                            params={"query": sparql_query},
                            headers={'Accept': 'application/sparql-results+json'})

    if response.status_code == 200:
        movies_data = response.json()['results']['bindings']
        return render_template('movies.html', data=movies_data)
    else:
        return render_template('empty.html', data={"data": data_iso_formatada})

@app.route('/movies/<title>')
def movie(title):
    sparql_query = f"""
    PREFIX cinema: <http://rpcw.di.uminho.pt/2024/cinema/>
    SELECT ?title ?release_date ?duration ?actor_name ?actor_birthdate ?musician_name WHERE {{
        ?film a cinema:Film ;
            cinema:title "{title}" ;
            cinema:releaseDate ?release_date ;
            cinema:duration ?duration ;
            cinema:hasActor ?actor ;
            cinema:hasMusic ?musician .
        ?actor cinema:name ?actor_name ;
            cinema:birthdate ?actor_birthdate .
        ?musician cinema:name ?musician_name .
    }}
    """

    response = requests.get(graphdb_endpoint,
                            params={"query": sparql_query},
                            headers={'Accept': 'application/sparql-results+json'})

    if response.status_code == 200:
        movie_data = response.json()['results']['bindings'][0]
        return render_template('movie.html', entry=movie_data)
    else:
        return render_template('empty.html', data={"data": data_iso_formatada})

if __name__ == '__main__':
    app.run(debug=True)