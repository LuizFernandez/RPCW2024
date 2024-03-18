# TPC5

**Objetivo**: Construir um dataset sobre o cinema

No ficheiro *dbpedia_movies.py*, lança uma query SPARQL ao *dbpedia* e pede informações referentes aos filmes. Nessa queries são pedidos:

- **URI** - uri do filme;
- **Designacao** - Nome do filme;
- **Duracao** - Duração do filme em segundos;
- **Atores** - Lista de Atores que aparecem no filme;
- **Escritores** - Lista de Escritos do filme;
- **Diretor** - Lista de Diretores do filme;
- **Musico** - Lista de Compositores da musica do filme;

Destes parâmetros todos, atores, escritores, diretores e musicos, são campos opcionais para alguns filmes, ou seja, em alguns casos não apresentam um valor associado a esses campos.

No ficheiro *dbpedia_actors.py*, envia-se uma query SPARQL para pedir informações referentes a todos os atores. Informações:

- **URI** - uri do ator;
- **nome** - Nome do ator;
- **Filmes** - Lista de Filmes em que o ator atuou;

Tal como no caso anterior, pode haver atores que não apresentem qualquer tipo de filmes.

No final tudo é junto no *dataset* **Cinema.json*