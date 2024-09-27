import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


import os
import google.generativeai as genai
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key = os.environ['OPENAI_API_KEY'],
    api_version = '2024-06-01',
    azure_endpoint = os.environ['OPENAI_API_BASE']
)

def embed_oai(content):
    return client.embeddings.create(
        input=content,
        model="text-embedding-3-large"
    ).data[0].embedding

def embed_gcp(content):
    return genai.embed_content(
        model="models/text-embedding-004",
        content=content,
        #task_type="retrieval_document",
        #title="Embedding of single string"
    )["embedding"]


with open("chunk_decomp.txt","r") as f:
    chunk_decomp = f.read()

with open("chunk_reveng.html","r") as f:
    chunk_reveng = f.read()

with open("chunk_pypdf.txt","r") as f:
    chunk_pypdf = f.read()

queries = [
    "Is there statistical significance between groups about question Q1(g)?",
    "What is the biggest percentage point difference between university and school groups in any single response category?",
    "Which question showed the most statistically significant difference between groups?",
    "How many degrees of freedom were used for all the chi-squared tests?",
    "Which question showed no statistically significant difference between groups?"
]


emb_gcp_decomp = embed_gcp(chunk_decomp)
emb_gcp_reveng = embed_gcp(chunk_reveng)
emb_gcp_pypdf = embed_gcp(chunk_pypdf)


emb_oai_decomp = embed_oai(chunk_decomp)
emb_oai_reveng = embed_oai(chunk_reveng)
emb_oai_pypdf = embed_oai(chunk_pypdf)

def cosinesim(a,b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a.T,b)/(np.linalg.norm(a)*np.linalg.norm(b))

def euclidean(a,b):
    return np.sqrt(np.sum((a-b)**2 for a,b in zip(a,b)))

data = {"query":[],"cosine":[],"euclidean":[],"approach":[],"embedding":[]}


for query in queries:

    print("\n\n ####\nQUERY:",query)

    emb_gcp_query = embed_gcp(query)
    emb_oai_query = embed_oai(query)

    data["query"].append(queries.index(query))
    data["cosine"].append(cosinesim(emb_gcp_decomp,emb_gcp_query))
    data["euclidean"].append(euclidean(emb_gcp_decomp,emb_gcp_query))
    data["approach"].append("decomp")
    data["embedding"].append("gcp")

    data["query"].append(queries.index(query))
    data["cosine"].append(cosinesim(emb_oai_decomp,emb_oai_query))
    data["euclidean"].append(euclidean(emb_oai_decomp,emb_oai_query))
    data["approach"].append("decomp")
    data["embedding"].append("oai")





    data["query"].append(queries.index(query))
    data["cosine"].append(cosinesim(emb_gcp_reveng,emb_gcp_query))
    data["euclidean"].append(euclidean(emb_gcp_reveng,emb_gcp_query))
    data["approach"].append("reveng")
    data["embedding"].append("gcp")

    data["query"].append(queries.index(query))
    data["cosine"].append(cosinesim(emb_oai_reveng,emb_oai_query))
    data["euclidean"].append(euclidean(emb_oai_reveng,emb_oai_query))
    data["approach"].append("reveng")
    data["embedding"].append("oai")





    data["query"].append(queries.index(query))
    data["cosine"].append(cosinesim(emb_gcp_pypdf,emb_gcp_query))
    data["euclidean"].append(euclidean(emb_gcp_pypdf,emb_gcp_query))
    data["approach"].append("pypdf")
    data["embedding"].append("gcp")

    data["query"].append(queries.index(query))
    data["cosine"].append(cosinesim(emb_oai_pypdf,emb_oai_query))
    data["euclidean"].append(euclidean(emb_oai_pypdf,emb_oai_query))
    data["approach"].append("pypdf")
    data["embedding"].append("oai")

    print(f"\n------------ GCP EMBEDDINGS ({len(emb_gcp_query)} dimensional space ) -------------")

    print("\n\n COSINE SIMILARITY (higher the better)")
    print("query against decomp",cosinesim(emb_gcp_decomp,emb_gcp_query))
    print("query against reveng",cosinesim(emb_gcp_reveng,emb_gcp_query))
    print("query against pypdf",cosinesim(emb_gcp_pypdf,emb_gcp_query))

    print("\n\n EUCLIDEAN DISTANCE (lower the better)")
    print("query against decomp",euclidean(emb_gcp_decomp,emb_gcp_query))
    print("query against reveng",euclidean(emb_gcp_reveng,emb_gcp_query))
    print("query against pypdf",euclidean(emb_gcp_pypdf,emb_gcp_query))



    print(f"\n\n------------ OAI EMBEDDINGS ({len(emb_oai_query)} dimensional space ) -------------")

    print("\n\n COSINE SIMILARITY (higher the better)")
    print("query against decomp",cosinesim(emb_oai_decomp,emb_oai_query))
    print("query against reveng",cosinesim(emb_oai_reveng,emb_oai_query))
    print("query against pypdf",cosinesim(emb_oai_pypdf,emb_oai_query))

    print("\n\n EUCLIDEAN DISTANCE (lower the better)")
    print("query against decomp",euclidean(emb_oai_decomp,emb_oai_query))
    print("query against reveng",euclidean(emb_oai_reveng,emb_oai_query))
    print("query against pypdf",euclidean(emb_oai_pypdf,emb_oai_query))


df_queries = pd.DataFrame({"query":queries})
df_results = pd.DataFrame(data)



##### PLOTTING

vendor="oai"
sim="cosine"

df_plot = (
    df_results
    .loc[lambda x: x["embedding"]=="oai"]
    .sort_values(["query",sim],ascending=sim=="euclidean")[["query",sim,"approach"]]
    .pivot(index="query",columns="approach",values=sim)
)

df_plot.index = df_plot.index+1
df_plot.columns.name = "Approach"
df_plot.index.name = "Query"
df_plot = df_plot.rename(columns={"decomp":"Decomposition","reveng":"Rev. Engineering"})


df_plot.plot.bar(color=['red','green','blue'])
plt.title("Similarity between queries and chunks embeddings")
plt.ylim([df_plot.min().min()*0.9,df_plot.max().max()*1.1])
plt.ylabel(sim[0].upper()+sim[1:])
plt.xticks(rotation=0)
plt.show()


