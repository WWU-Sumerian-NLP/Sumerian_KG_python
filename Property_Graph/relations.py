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

class ParseRelationTypes:
    def __init__(self, relationType, subject_name, object_name, tablet_num, 
                providence, period, dates_referenced, subject_tag, object_tag) -> None:
        self.relationType = str(relationType)  #person:delivers_animal 
        self.Subject = self.createEntityNode(subject_tag, subject_name, tablet_num)
        self.Object = self.createEntityNode(object_tag, object_name, tablet_num)
        self.Relationship = self.createRelationshipNode(providence, period, dates_referenced)

    def parse_relation(self):
        return self.relationType.split(":")

    def createEntityNode(self, entity_tag, entity_name, tablet_num):
        if 'PN' in entity_tag or 'FOR' in entity_tag:
            return Person(entity_name, tablet_num)
        elif 'ANIM' in entity_tag: 
            return Animal(entity_name, tablet_num)
        

    def createRelationshipNode(self, providence, period, dates_referenced):
        return Relationship(self.Subject.get_neo4j_node(), self.relationType, self.Object.get_neo4j_node(), 
        providence=providence, period=period, dates_referenced=dates_referenced)

#PN - Personal Name Tag
class Person:
    def __init__(self, name, tablet_num) -> None:
        self.name = str(name)
        self.tablet_num = str(tablet_num)   

    def get_neo4j_node(self):
        neo4j_node = Node("Person", pk=get_random_number(), name=self.name, tablet_num=self.tablet_num)   
        return neo4j_node


class Animal:
    def __init__(self, name, tablet_num):
        self.name = str(name)
        self.tablet_num = str(tablet_num)
  
    def get_neo4j_node(self):
        neo4j_node = Node('Animal', pk=get_random_number(), name=self.name, tablet_num=self.tablet_num)
        return neo4j_node