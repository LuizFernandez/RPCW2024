# TPC6

**Objetivo**: Carregar o _dataset_ obtido no TPC5 para o repositorio e construir uma aplicação Web para ver o Cinemas

O ficheiro _parseTTL.py_ está responsavel por ele o _dataset_ obtido no ultimo TPC e de carregar para a ontologia, neste caso, contruir os individuos consuante os valores existentes.

Após o ficheiro _cinema_populated.ttl_ estiver pronto, ele é carregado para o repositorio no graphDB para posteriormente, poder-se criar SPARQL Queries para a aplicação.

Por fim os ficheiro dentro da pasta _app_ estão reponsáveis por efetuar os pedidos ao repositorio e de fazer _display_ desses valores na _Front-End_, tal como estruturar como os valores obtidos estão dispostos.
