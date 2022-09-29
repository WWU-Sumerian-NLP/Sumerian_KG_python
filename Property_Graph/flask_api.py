from flask import Flask 
from flask_cors import CORS, cross_origin
from create_pg import GraphDataCreator

api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'

@api.route('/pipeline', methods=['POST'])
@cross_origin()
def build_graph():
    response_body = {
        "name": "this is a test"
    }
    # gdc = GraphDataCreator("~/Desktop/urr3-drehem-KG/Data_Pipeline_go/IE_Extractor/output/urr3_ie_annotations.tsv") #fix path
    gdc = GraphDataCreator("~/Desktop/urr3-drehem-KG/gRPC_Server_go/cmd/urr3_ie_annotations.tsv") #fix path
    gdc.create_graph()
    return response_body

if __name__=='__main__':
    api.run(host='localhost', port=8080)