import pandas as pd
import sys

import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 14})


df_results = pd.read_csv("../../experiment/embedding_comparisons.csv",index_col=0)


vendor="oai" #default
sim="cosine" #default
show_plot = False #default

flag = None
for i,arg in enumerate(sys.argv):
    if i==0:
        continue
    if arg[0] == "-": # flag
        flag = arg.split("-")[-1][0]

        if flag[0] == 'p': # plot flag
            show_plot=True
            flag=None

    else: # value of flag
        if flag[0] == 'v': # vendor flag
            for v in list(df_results["embedding"].unique()) :
                if arg in v:
                    vendor = v
                
        elif flag[0] == 's': # similarity flag
            for s in ["cosine","euclidean"]:
                if arg in s:
                    sim = s

        flag=None

print(f"Comparing {vendor} embeddings with {sim} similarity")



df_plot = (
    df_results
    .loc[lambda x: x["embedding"]=="oai"]
    .sort_values(["query",sim],ascending=sim=="euclidean")[["query",sim,"approach"]]
    .pivot(index="query",columns="approach",values=sim)
)

df_plot.index = df_plot.index+1
df_plot.columns.name = "Approach"
df_plot.index.name = "Question #"

reveng_format = None
with open("../../prompts/reverse_engineering.txt","r") as f:
    prompt = "\n".join([row for row in f.read().split("\n") if len(row) > 0 and row[0] != '#'])
    if "json" in prompt.lower():
        reveng_format = "JSON"
    elif "markdown" in prompt.lower():
        reveng_format = "Markdown"
    elif "html" in prompt.lower():
        reveng_format = "HTML"
    
    if reveng_format:
        reveng_format = f" ({reveng_format})"

df_plot = df_plot.rename(columns={"decomp":"Decomposition","reveng":f"Rev. Engineering{reveng_format}","pypdf": "PyPDF"})


fig = plt.figure(figsize=(10,5))
ax = plt.gca()

df_plot.plot.bar(ax=ax, color=['#F8A39E','#A5C1DD','#C2E8B9'])

plt.title("Similarity between queries and chunks embeddings")
plt.ylabel(sim[0].upper()+sim[1:])

plt.ylim([df_plot.min().min()*0.9,df_plot.max().max()*1.1])
plt.xticks(rotation=0)

plt.tight_layout(pad=0)
plt.savefig("similarity_comp.png", dpi=200)

if show_plot:
    plt.show()

