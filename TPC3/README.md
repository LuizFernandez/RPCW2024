# TPC3

## Autor
Luís Miguel Teixeira Fernandes

## Data 
26/02/2024

## UC
RPCW

### Resumo

1. Ler o dataset e criar uma ontologia
   1. Criar duas classes:
      1. **Cidade** => Grande a informação relativa às cidades
      2. **Ligação** => Como as ligações tem um propriedades (distância) é mais correto defini-la como Classe do que *Object Propertie* entre duas **Cidades**
   2. Adicionar *Data Properties* e *Object Properties* a cada classe
2. Povoar a ontologia com ajuda de um script escrito em *python* (*city_connection.py*)
3. Com a ontologia criada e povoada, carrega-la para o graphDB para assim criar as queries.

4. As queries criadas estão todas colocadas no ficheiro **queries.txt**, cada uma associada ao objetivo da sua execução.