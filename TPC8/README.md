# TPC8

**Objetivo** Fazer *paser* dos ficheiros xml e popular uma ontologia com os dados extraídos dos xml

1. Inicialmente, os dados são extraidos dos ficheiros xml, usando a função *import_xml2data* que irá construir uma lista de pessoas, que são os dados a popular as ontologias.
2. Após o parser dos xmls, usa-se uma nova função (*import_data2ttl*) que irá popular as ontologias (*royal.ttl* e *biblia.ttl*) usando os dados obtidos pelo xml na função anterior.
3. No final, os dados serão carregados para os ficheiros correspondentes.