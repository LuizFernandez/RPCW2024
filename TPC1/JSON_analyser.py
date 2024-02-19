import json
import sys

f = open(sys.argv[1])
db = json.load(f)
f.close()

keys = list(db[0].keys())
info = {}

len_key = 0

for key in keys:
    info[key] = {"missing_values": 0, "values": []}
    if(len(key) > len_key):
        len_key = len(key)

for data in db:
    for key in list(data.keys()):
        if(data[key] == ""):
            info[key]["missing_values"] += 1
        info[key]["values"].append(data[key])

print("+" + "-" * (len_key + 19 + 25) + "+")
print("| Attribute " + " " * (len_key - 10 + 1) + " | Unique Values (%) | Missing Values (%) |")
print("+" + "-" * (len_key + 19 + 25) + "+")
for key in list(info.keys()):
    uniqueValues = len(set(info[key]["values"]))
    totalValues = len(info[key]["values"])
    percentageUnique = uniqueValues / totalValues
    percentageMissing = info[key]["missing_values"] / totalValues
    print(f"| {key} " + " " * (len_key - len(key)) + f" | {percentageUnique:<17.2%} | {percentageMissing:<18.2%} |")

print("+" + "-" * (len_key + 19 + 25) + "+")


