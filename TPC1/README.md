# Script para Ontologia de Plantas

## Autor
Luís Miguel Teixeira Fernandes

## Data 
19/02/2024

## UC
RPCW

### Resumo

1. Usar o ficheiro JSON_anayser.py, para ver quais atributos cada valor tinha, neste caso, as keys de cada dado.
2. Com esses atributos identifiquei quais seriam as classes da Ontologia, e posteriormente quais seria as suas *Data properties* tal como as *Object properties* entre as diferentes classes.
3. Sendo assim, identifiquei 3 classes principais:
   1. "Plantas": é a classe principal da Ontologia, define cada objeto planta que existe no dataset.
   2. "Espécie": Contêm as DPs "Espécie" e "Nome Científico", e tem um relação OP com "Planta"
   3. "Rua": Contêm as DPs repalcionadas com ruas, e um OP com Planta;
   
### Ficheiros

- [`plantas.json`](plantas.json): Arquivo *JSON*, fornecido pelo professor, contendo dados sobre plantas.

- [`out.ttl`](out.ttl): output do script, com os individuos criados.

- [`plantas.ttl`](plantas.ttl): Ficheiro *Turtle* final, com toda a ontologia.

- [`JSON_analyser.py`](JSON_analyser.py): *Script* em *Python* que lê um *dataset* e retorna uma tabela com todos os atributos, mais percentagem de *missing_values* e *unique_values*.

- [`plantas_script.py`](plantas_script.py): *Script* em *Python* que lê o *dataset* e cria os individuos da Ontologia.


