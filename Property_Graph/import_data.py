from py2neo import Graph
import pandas as pd 
from relations import ParseRelationTypes

class FileInput:
    def __init__(self, path_to_file):
        self.df = pd.read_csv(path_to_file, delimiter="\t") 
    
    def parse_data(self):
        for _, row in self.df.iterrows():
            neo4j_graph = Graph(password="password")
            if (row.NameTag == "PN" or row.NameTag == "DN") and (row.ToTag == "PN" or row.ToTag == "DN"):
                #subject = Name
                #object = to
                parsedRelationTypes = ParseRelationTypes(neo4j_graph, row.Relation, row.Name, row.To, row.TabletID, row.NameTag, row.ToTag)
                subject, object = parsedRelationTypes.Subject, parsedRelationTypes.Object
                relationship = parsedRelationTypes.createRelationshipNode(subject, object, "no providence", "no period", "no dates referenced")
                print(relationship)
                neo4j_graph.create(relationship)

fi = FileInput("relation_data.tsv") #fix path
fi.parse_data() 

'''
Add module that loads up the providence, period, and dates referenced into a giant map (this info can be
easily extracted using existing pipeline scripts). And adds them up here 

'''

#TabletID, Name, Relation, To, NameTag, RelationTag, ToTag
# P100001, sza3-gu4, dummu, x-x, PN, N, PN