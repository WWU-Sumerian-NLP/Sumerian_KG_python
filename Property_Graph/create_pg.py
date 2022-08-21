from py2neo import Graph
import pandas as pd 
from relations import ParseRelationTypes




class GraphDataCreator:
    def __init__(self, pathToRelationData):
        self.pathToRelationData = pathToRelationData
        self.df = pd.read_csv(self.pathToRelationData, sep="\t")
        # self.df.drop_duplicates() #investigate later 
        # self.df.sort_values(by=["tablet_num"], inplace=True)
    
    def create_graph(self): #in the future, this will be create nodes, and then we create the graph
        neo4j_graph = Graph(password="password")
        for _, row in self.df.iterrows():
            parsedRelationTypes = ParseRelationTypes(neo4j_graph, row.relation_type, row.subject, row.object, row.tablet_num, row.providence,
            row.period, row.dates_referenced, row.subject_tag, row.object_tag)
            neo4j_graph.create(parsedRelationTypes.Relationship)
        
 

gdc = GraphDataCreator("~/Desktop/urr3-drehem-KG/Data_Pipeline_go/IE_Extractor/output/ie_data.tsv") #fix path
# gdc = GraphDataCreator("test_relation.tsv")
gdc.create_graph()