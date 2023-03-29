import os
import pandas as pd
import json
dir= r'D:\PokemonGAN_project\Pokemon_dataset\dataset'
pokemonTypesCsv = r'D:\PokemonGAN_project\Pokemon_dataset\Pokemon_types_csv\pokemon.csv'

df = pd.read_csv(pokemonTypesCsv)

Name_to_type_dict1= pd.Series(df.Type1.values,index =df.Name.values).to_dict()
Name_to_type_dict2= pd.Series(df.Type2.values,index =df.Name.values).to_dict()

pokemon_type_labels =list(set(Name_to_type_dict1.values()))

labelposlist= list(range(len(pokemon_type_labels)))

type_to_label_dict= dict(zip(pokemon_type_labels,labelposlist))
folderNames_pokemonNames = os.listdir(dir)

"""
Format Labels as such
{
        "labels": [
            ["00000/img00000000.png",6],
            ["00000/img00000001.png",9],
            ... repeated for every image in the datase
            ["00049/img00049999.png",1]
        ]
}
"""
label_dict= {"labels":[]}
label_list=[]

#Messy Way to deal with Farfetch'd
for x in folderNames_pokemonNames:
    directory =os.path.join(dir,x)
    cur_directory= os.listdir(directory)
    for item in cur_directory:
        if ('.png' in item) or ('.jpg' in item):
            label_empty_list = [0]*len(labelposlist)
            cur_item = os.path.join(directory,item)
            try:
                pos1 = type_to_label_dict[Name_to_type_dict1[x]]
            except:
                if x == "Farfetchd":
                    x ="Farfetch'd"
                    pos1 = type_to_label_dict[Name_to_type_dict1[x]]
                print()
            label_empty_list[pos1]=1
            try:
                pos2 = type_to_label_dict[Name_to_type_dict2[x]]
                label_empty_list[pos2]=1

            except KeyError:
                pos2 = None
                pass
            label_list.append([cur_item,label_empty_list])


label_dict['labels'] = label_list

with open('dataset.json','w') as fp:
    json.dump(label_dict,fp)








