from create_pg import GraphDataCreator

gdc = GraphDataCreator("~/Desktop/urr3-drehem-KG/Data_Pipeline_go/IE_Extractor/output/all_ie_data.tsv") #fix path
gdc.create_graph()