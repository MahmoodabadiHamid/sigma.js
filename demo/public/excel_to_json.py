import random
import pandas as pd
import hazm
import networkx as nx
import random
from itertools import chain 


""" READING AND CLEANING THE EXCEL"""
norm = hazm.Normalizer()
excel_file = 'data.xlsx'

df_edges = pd.read_excel(excel_file, sheet_name=0, header=0)
for i in range(len(df_edges)):
    df_edges.iloc[i]['source'] = norm.normalize(df_edges.iloc[i]['source']).replace('\u200c', ' ').strip()
    df_edges.iloc[i]['destination'] = norm.normalize(df_edges.iloc[i]['destination']).replace('\u200c', ' ').strip()

edges = []#df_edges.values.tolist()
for item in df_edges.values.tolist():
    edges.append([norm.normalize(item[0]).replace('\u200c', ' ').strip(), norm.normalize(item[1]).replace('\u200c', ' ').strip()])


df_nodes = pd.read_excel(excel_file, sheet_name=1, header=0)
df_nodes['cluster'] = df_nodes['cluster'].apply(str)
nodes = df_nodes.to_dict('records')

for i in range(len(nodes)):
	nodes[i]['key'] = norm.normalize(nodes[i]['key']).replace('\u200c', ' ').strip()
	nodes[i]['label'] = norm.normalize(nodes[i]['label']).replace('\u200c', ' ').strip()
	nodes[i]['tag'] = norm.normalize(nodes[i]['tag']).replace('\u200c', ' ').strip()
""" __________________________________________________ """




""" CHECK IF FOR ANY BUG IN EXCEL GENERATION """
edges_check = set(list(chain.from_iterable(edges)))
nodes_check =  set([i['key'] for i in nodes])

if edges_check != nodes_check:
    for item in nodes_check.symmetric_difference(edges_check):
        print(item)
    raise ValueError("Error: Inconsistent Lengths of Edges and Nodes. \n Description: The values provided in the edges and nodes are not equal. Please review the printed values.")
""" __________________________________________________ """







""" START TO VISUALIZING DATA """ 
G=nx.from_pandas_edgelist(df_edges, 'source', 'destination')
pos = nx.fruchterman_reingold_layout(G)
#pos = nx.circular_layout(G)
#pos = nx.random_layout(G)
#pos = nx.spectral_layout(G)
#pos = nx.spring_layout(G)
#pos = nx.graphviz_layout(G)
#pos = nx.pygraphviz_layout(G)
#pos = nx.graphviz_layout(G)
#pos = nx.pydot_layout(G)
#pos = nx.bipartite_layout(G)
#pos = nx.circular_layout(G)
#pos = nx.kamada_kawai_layout(G)
#pos = nx.planar_layout(G)
#pos = nx.random_layout(G)
#pos = nx.rescale_layout(G)
#pos = nx.shell_layout(G)
#pos = nx.spring_layout(G)
#pos = nx.spectral_layout(G)
#pos = nx.spiral_layout(G)
#pos = nx.multipartite_layout(G)

for key, position in pos.items():
    for dic in nodes:
        if dic['key'] == key:
                dic['x']= list(position)[0]
                dic['y']= list(position)[1]
                dic['score']= G.degree()[key]
                #print(key)
        elif 'ابزارها' in key and 'ابزارها' in dic['key']:
            #print('[', "'", key, "'", ",", "'", dic['key'],"'", "]")
            pass



clusters_key=[]
clusters = ""
random.seed(2)
r = lambda: random.randint(0,255)
for i in zip(df_nodes['cluster'].values, df_nodes['tag'].values):
    if str(i[0]) not in clusters_key:
        random_color = '#%02X%02X%02X' % (r(),r(),r())
        clusters+= ", "+ str({"key": str(i[0]), "color": random_color, "clusterLabel": i[1]})
        clusters_key.append(str(i[0]))
clusters = clusters[1:]

tags = []
for dic in nodes:
    tags.append(dic['tag'])
tags = list(set(tags))

json_str = """{
  "nodes": 
  """ + str(nodes) + """ ,
  "edges": """ + str(edges) + """  ,
  "clusters": [ """+clusters+""" ],
  "tags": [
    {"key": "حسابداری و حسابرسی در بازار سرمایه اسلامی", "image": "hesabdari.png" },
    {"key": "مدیریت ریسك در بازار سرمایه اسلامی", "image": "risk.png" },
    {"key": "قوانین و مقررات در بازار سرمایه اسلامی", "image": "ghavanin.png" },
    {"key": "سایر", "image": "sayer.png" },
    {"key": "نهادهای مالی فعال در بازار سرمایه اسلامی", "image": "nahad.png" }, 
    {"key": "طبقه بندی بازار سرمایه اسلامی", "image": "tabaghebazar.png" },
    {"key": "مبانی، اصول و مفاهیم بازار سرمایه اسلامی", "image": "mabani.png" },
    {"key": "ابزارهای مالی اسلامی", "image": "abzar.png" },
    {"key": "تشکل های خود انتظام بازار سرمایه", "image": "bazar.png" },
    {"key": "معاملات و قراردادها", "image": "bazar.png" }
  ]}"""

_ = open('dataset.json', 'w', encoding='utf-8').write(str(json_str).replace("'", '"'))
