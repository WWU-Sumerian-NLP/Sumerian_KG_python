import random 
import csv
from py2neo import Graph, Node, Relationship

def get_random_number():
    return random.randint(100000000, 1000000000)

'''
Ex: 

relationType: person:delivers_animal  --> which is identified by mu-kux(DU)
subject_name: ur-nigar
object_name: sila4
tablet_num: P100001

'''

#temporary maps Entity labels to user readable labels
temp_global_dict = {
    "PN": "Person",
    "PN_1": "Person",
    "PN_2": "Person",
    "ANIM": "Animal",
    "DN": "Divine"
}
#load files 
reader = csv.reader(open('/Users/hanselguzman-soto/Desktop/urr3-drehem-KG/Data_Pipeline_go/Annotation_lists/NER_Lists/foreigners_ner.csv', 'r'))
FOREIGNER_DICT = {}
for row in reader:
   k, v = row
   FOREIGNER_DICT[k] = v


class ParseRelationTypes:
    def __init__(self, graph, relationType, subject_name, object_name, tablet_num, 
                subject_tag, object_tag) -> None:
        self.graph = graph 
        self.relationType = str(relationType)  #person:delivers_animal 
        self.Subject = self.createEntityNode(subject_tag, subject_name, tablet_num) #should be node objects
        self.Object = self.createEntityNode(object_tag, object_name, tablet_num) # should be node objects
        # self.Relationship = self.createRelationshipNode(self.Subject, self.Object, providence, period, dates_referenced)

    def parse_relation(self):
        return self.relationType.split(":")


    def createEntityNode(self, entity_tag, entity_name, tablet_num):
        #first check if entity exists and just returns taht
        existing_entity = self.checkIfEntityExistsInGraph(entity_tag, entity_name)
        if existing_entity is not None:
            return existing_entity

        #otherwise, create new entity node based on entity_tag
        if 'PN' in entity_tag or 'FOR' in entity_tag:
            return Person(entity_name, tablet_num).create_neo4j_node()
        elif 'DN' in entity_tag:
            return Divine(entity_name, tablet_num).create_neo4j_node()
        elif 'ANIM' in entity_tag: 
            return Animal(entity_name, tablet_num).create_neo4j_node()
        
    def checkIfEntityExistsInGraph(self, entity_tag, entity_name):
        if entity_tag == "ANIM": #animals can be duplicated 
            return None 
        return self.graph.nodes.match(temp_global_dict[entity_tag], name=entity_name).first()

    def createRelationshipNode(self, SubjectNode, ObjectNode, providence, period, dates_referenced):
        return Relationship(SubjectNode, self.relationType, ObjectNode, 
        name=self.relationType, providence=providence, period=period, dates_referenced=dates_referenced)

#PN - Personal Name Tag
class Person:
    def __init__(self, name, tablet_num) -> None:
        self.name = str(name)
        self.tablet_num = str(tablet_num)

    def is_Foreigner(self, foreginer_dict):
        if self.name in foreginer_dict:
            self.neo4j_node["isForeigner"] = "true"

    def create_neo4j_node(self):
        self.neo4j_node = Node("Person", name=self.name, tablet_num=self.tablet_num)
        self.is_Foreigner(FOREIGNER_DICT) 
        return self.neo4j_node
    

#DN - Divine Name Tag
class Divine:
    def __init__(self, name, tablet_num):
        self.name = str(name)
        self.tablet_num = str(tablet_num)

    def create_neo4j_node(self):
        neo4j_node = Node("Divine", name=self.name, tablet_num=self.tablet_num)
        return neo4j_node

class Animal:
    def __init__(self, name, tablet_num):
        self.name = str(name)
        self.tablet_num = str(tablet_num)
  
    def create_neo4j_node(self):
        neo4j_node = Node('Animal', name=self.name, tablet_num=self.tablet_num)
        return neo4j_node