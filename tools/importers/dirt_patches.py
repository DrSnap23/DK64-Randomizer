"""Convert Dirt Patch CSV into a python list."""
import csv
import re

with open("dirt_patches.csv", newline="") as csvfile:
    patch_data = csv.reader(csvfile, delimiter=",", quotechar="|")
    patch_data_json = []
    for idx, row in enumerate(patch_data):
        if idx > 0:
            patch_data_json.append({"map": row[1], "subname": row[3], "name": row[4], "coords": [float(row[5]), float(row[6]), float(row[7])], "rot": int(row[9]), "vanilla": row[10] == "YES"})
    print(f"{len(patch_data_json)} patches found")
    print("-----------------")
    for x in patch_data_json:
        vanilla_text = ""
        if x["vanilla"]:
            vanilla_text = ", vanilla=True"
        subname = x["subname"]
        if " - " in subname:
            pre = subname.split(" - ")[0]
            post = subname.split(" - ")[1].split(": ")[0]
            post = re.sub(r"((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))", r" \1", post)
            subname = f"{pre} - {post}: "
        name = f"{subname}{x['name']}"
        print(f"DirtPatchData(name=\"{name}\", map_id=Maps.{x['map']}, x={x['coords'][0]}, y={x['coords'][1]}, z={x['coords'][2]}, rotation={x['rot']}{vanilla_text}),")