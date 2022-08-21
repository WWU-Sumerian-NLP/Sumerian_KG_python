import random 
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

#global variable
unique_entity_dict = {}

class ParseRelationTypes:
    def __init__(self, graph, relationType, subject_name, object_name, tablet_num, 
                providence, period, dates_referenced, subject_tag, object_tag) -> None:
        self.graph = graph 
        self.relationType = str(relationType)  #person:delivers_animal 
        self.Subject = self.createEntityNode(subject_tag, subject_name, tablet_num) #should be node objects
        self.Object = self.createEntityNode(object_tag, object_name, tablet_num) # should be node objects


        self.Relationship = self.createRelationshipNode(self.Subject, self.Object, providence, period, dates_referenced)

    def parse_relation(self):
        return self.relationType.split(":")

    def checkIfEntityExists(self, entity_name):
        existing_entity = self.graph.nodes.match('Person', name=entity_name).first()
        if existing_entity is not None:
            return existing_entity #node object

    def createEntityNode(self, entity_tag, entity_name, tablet_num):
        if 'PN' in entity_tag or 'FOR' in entity_tag:
            existing_person = self.graph.nodes.match('Person',name=entity_name).first()
            print(existing_person)
            print(type(existing_person))
            if existing_person is not None:
                return existing_person
            else:
                return Person(entity_name, tablet_num).node
        elif 'ANIM' in entity_tag: 
            return Animal(entity_name, tablet_num).node
        

    def createRelationshipNode(self, SubjectNode, ObjectNode, providence, period, dates_referenced):
        return Relationship(SubjectNode, self.relationType, ObjectNode, 
        name=self.relationType, providence=providence, period=period, dates_referenced=dates_referenced)

#PN - Personal Name Tag
class Person:
    def __init__(self, name, tablet_num) -> None:
        self.name = str(name)
        self.tablet_num = str(tablet_num)
        self.node = Node("Person", name=self.name, tablet_num=self.tablet_num)    

    def create_neo4j_node(self):
        neo4j_node = Node("Person", name=self.name, tablet_num=self.tablet_num)   
        self.node = neo4j_node


class Animal:
    def __init__(self, name, tablet_num):
        self.name = str(name)
        self.tablet_num = str(tablet_num)
        self.node =  Node('Animal', name=self.name, tablet_num=self.tablet_num)
  
    def get_neo4j_node(self):
        neo4j_node = Node('Animal', name=self.name, tablet_num=self.tablet_num)
        self.node = neo4j_node