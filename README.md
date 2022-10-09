# Sumerian Knowledge Graphs API
This is our API that takes data generated from our NLP libraries to create a knowledge graph and store it in Neo4j

## Description

Our API utilizes relations from relation extraction service in our NLP library to build knowledge graph which is ingested in a neo4j local instance </br>

This picture below shows the sample schema for a person node in our neo4jgraph </br>
![person_schema](https://github.com/WWU-Sumerian-NLP/images/blob/master/kg_schema.png)


## Project structure

```
|__ Data_Collection/ --> Contains  modules to retrieve data.
        |__ CLDI_Downloader/ --> Module for downloading data from various sources such as CLDI website, CLDI daily dumps, github repos and gdrive folder.

|__ NER_Models/ --> A user can put an ATF file and can provide the path while calling pipeline.py file

|__ Property_graph/ --> Our api which builds a knowledge graph in a local neo4j instance

|__ sumerian_tablets/ --> setup.sh will init this directory which will store all of the .atf sumerian tablet data


## Authors
Hansel Guzman-Soto (https://www.linkedin.com/in/hansel-guzman-soto/)
