from flask import Flask 
from create_pg import GraphDataCreator

api = Flask(__name__)

@api.route('/build_graph')
def build_graph():
    response_body = {
        "name": "this is a test"
    }
    gdc = GraphDataCreator("~/Desktop/urr3-drehem-KG/Data_Pipeline_go/IE_Extractor/output/urr3_ie_annotations.tsv") #fix path
    # gdc = GraphDataCreator("test_relation.tsv")
    gdc.create_graph()
    return response_body