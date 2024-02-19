import json

f = open("plantas.json")
db = json.load(f)
f.close()

especie = {}
db1 = db

ttl = ""

for data in db1:
    value = data["Espécie"]
    if value not in especie.keys():
        especie[value] = set()
    for data in db1:
        if data["Espécie"] == value:
            especie[value].add(data["Nome Científico"])
            db1.remove(data)

ttl = ""

for key in especie.keys():
    registo = f"""
###  http://rpcw.di.uminho.pt/2024/plantas#{key.replace(' ', '_')}
:{key.replace(' ', '_')} rdf:type owl:NamedIndividual ,
                         :Espécie ;
                :espécie "{key.replace(' ', '_')}" ;
                :nome_cientifico "{list(especie[key])[0].replace(' ', '_')}" .
"""
    ttl += registo

db2 = db
rua = {}

for data in db2:
    value = data["Código de rua"]
    if value not in rua.keys():
        rua[value] = {"Rua": data["Rua"], "Código de rua": value, "Local": data["Local"], "Freguesia": data["Freguesia"]}

for key in rua.keys():
    registo = f"""
###  http://rpcw.di.uminho.pt/2024/plantas#{rua[key]["Código de rua"]}
<http://rpcw.di.uminho.pt/2024/plantas#{rua[key]["Código de rua"]}> rdf:type owl:NamedIndividual ,
                                                         :Rua ;
                                                :código_de_rua "{rua[key]["Código de rua"]}" ;
                                                :freguesia "{(rua[key]["Freguesia"]).replace(" ", "_")}" ;
                                                :local "{(rua[key]["Local"]).replace(" ", "_")}" ;
                                                :rua "{(rua[key]["Rua"]).replace(" ", "_")}" .
"""
    ttl += registo

for planta in db:
    registo = f"""
    ###  http://rpcw.di.uminho.pt/2024/plantas#{planta["Id"]}
<http://rpcw.di.uminho.pt/2024/plantas#{planta["Id"]}> rdf:type owl:NamedIndividual ,
                                                          :Planta ;
                                                 :classificadoPor :{planta["Espécie"].replace(" ", "_")};
                                                 :localizadoEm <http://rpcw.di.uminho.pt/2024/plantas#{planta["Código de rua"]}> ;
                                                 :caldeira "{planta["Caldeira"]}" ;
                                                 :data_atualização "{planta["Data de actualização"]}" ;
                                                 :data_plantação "{planta["Data de Plantação"]}" ;
                                                 :estado "{planta["Estado"]}" ;
                                                 :gestor "{planta["Gestor"]}" ;
                                                 :id "{planta["Id"]}" ;
                                                 :implantação "{planta["Implantação"]}" ;
                                                 :numero_intervenções "{planta["Número de intervenções"]}" ;
                                                 :numero_registo "{planta["Número de Registo"]}" ;
                                                 :origem "{planta["Origem"]}" ;
                                                 :tutor "{planta["Tutor"]}" .
    """
    ttl += registo

print(ttl)