# TPC4

1. elementos.html

   1. Acrescentar coluna com o grupo;
      - Alteração da Query que pede os elementos, para pedir também ou o nome do grupo ou o seu número;
   2. Grupo é um link para a página do grupo;
      - No ficheiro elements.html, adicionar um nova coluna _\<tr\>_ com um elemento _\<a\>_ com o nome/número do grupo para servir com link;
   3. O número atómico ou o nome é um link para a página do elemento;
      - A coluna do número atómica passa a ser um _\<a\>_

2. Grupos.html

   1. Listar Grupos;
      - Criar uma nova query que vá buscar os dados fundamentais de cada grupo, neste caso, nome e número (caso existam);
      - Criar um novo template _groups.html_ para fazer _display_ dos valores obtidos;
      - O nome e o número são _anchor_ para ir para o detalhes do grupo selecionado;

3. Grupo.html

   1. Informação do Grupo, Lista de elementos que pertencem ao grupo
      - Criar uma query que vá buscar, o nome, número e todos os elementos que pertencem a esse grupo;
      - Criar um template _group.html_ para demonstrar os valores obtidos pela query;

4. elemento.html
   1. Informação do elemento
      - Criar template _element.html_ para demonstrar os detalhes do elemento selecionado;
      - Criar uma query para obter os detalhes desejado do dado elemento para posteriormente serem apresentado;
