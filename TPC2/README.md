# TPC2

## Autor
Luís Miguel Teixeira Fernandes

## Data 
26/02/2024

## UC
RPCW

### Resumo

1. Ler o dataset e fazer algumas correções no dados
   1. Nos dados sobre os cursos, simplificar os instrumentos, em vez de ter o intrumento como um todo, apenas conter o ID
   2. Nos instrumentos, simplificar o nome da variável *#text* para nome
   3. Nos alunos, trocar o nome do intrumento para o seu ID, como também fazer correções relativas ao id do curso em que estão inscritos
   
2. Com a análise do dataset decidir que classes ter
   1. 3 classes principais:
      - **Aluno**
      - **Curso**
      - **Instrumento**
   2. Curso apresenta duas subclasses, de acordo com o grau de ensino (são disjuntas):
      - **Básico**: quando o id do curso apresenta *CB*
      - **Supletivo**: quando o id do curso aprenseta *CS*
   3. Instrumento tem uma subclasse **Tipo**, que por sua vez apresenta mais três subclasses que são disjuntas entre si
      - **Cordas**: instrumentos da família de cordas
      - **Sopro**: Instrumentos da família de sopro
      - **Outro**: Instrumentos de outras famílias

3. Com as classes definir as *Object Properties*
   1. **aprendeInstrumento**: relação entre **aluno** e **intrumento**
   2. **ensinaInstrumento**: relação entre **curso** e **instrumento**
   3. **inscritoEm**: relação entre **aluno** e **instrumento**
   
4. As subclasses de **Curso** são escolhidas através do seu id, usando a função *course_classification* que retorna o nome da subclass.

5. As subclasses de **Tipo**, são escolhidas conforme o instrumento. A função *instrument_classification* recebe o nome do instrumento, e conforme as famílias que tem conhecimento, verifica se o nome que recebeu está inserido nessas famílias, e retorna o nome da família.
   
5. Após este tratamento e a definição das *Classes*, *Data Properties* e das *Object Properties*, carregar os Individuos para o ficheiro *turtle*
