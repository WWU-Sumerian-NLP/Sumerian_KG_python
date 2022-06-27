from py2neo import Graph, Node, Relationship
import random
import pandas as pd 

data_path = "~/Desktop/urr3-drehem-KG/Data_Pipeline_go/CDLI_Extractor/output/new_pipeline.tsv" #fix path

def get_random_number():
    return random.randint(100000000, 1000000000)

def create_graph():
    df = pd.read_csv(data_path, sep="\t")
    df = df[df.relations.astype(str) != "nan"]
    df = df.drop_duplicates(subset=['relations'])
    for relation_tuple in df["relations"]:
        t1, t2, t3 = relation_tuple.split(" ")

        #animal node 
        animal_pk = get_random_number()
        animal_node = Node("Animal", pk=animal_pk, name=t1)

        #Person node
        person_pk = get_random_number()
        person_node = Node("Person", pk=person_pk, name=t2)

        #Relationship Node - Delivery 
        rel_delivery_node = Relationship(person_node, "deliveredBy", animal_node)
        graph.create(rel_delivery_node)
        #(ANIM, PN, DEL)
        print(t1, t2, t3)

graph = Graph(password="password")
create_graph()