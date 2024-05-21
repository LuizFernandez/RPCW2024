# Aferição / TPC7

**Objetivo** Fazer uma **API** de dados, para o conjunto de dados de alunos

1. Cria uma ontologia OWL para modelar o universo da avaliação de alunos registado no dataset fornecido:
   1. Classes: *Curso*, *Aluno*, *Exame* (Com três sub-classes, *Recurso*, *Especial* e *Normal*) e *TPC*;
   2. Criada relações entre a Classe *Aluno* com as restantes, e uma relação inversa das restantes para *Aluno*;
   3. Diversos atributos que caracterizam a Classe:
      1. Exemplo:
         1. Aluno: id, nome, projeto
         2. TPC: id, nota
         3. Exame: id, nota
         4. Curso: id, curso
2. Povoar a ontologia no *graphdb* através da utilização de um script, na qual primeiramente criou um ficheiro *ttl* com a ontologia + povoamento (Indivíduos) e carregar para um repositório.

3. Especificar queries **SPARQL**, que permitem obter diferentes valores da Base de dados (Queries definidas em queries.txt)

4. *Script* em python (*api.py*) é a **API** do sistema, na qual envia para o *browser* diversos dados em JSON, dependedo do endereço para o qual o browser faz o pedido.