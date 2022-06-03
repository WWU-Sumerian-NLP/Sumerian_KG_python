# Sumerian Knowledge Graphs for Urr III Drehem Data (KG)

## Project structure

```
|__ Data_Collection/ --> Contains  modules to retrieve data.
        |__ CLDI_Downloader/ --> Module for downloading data from various sources such as CLDI website, CLDI daily dumps, github repos and gdrive folder.

|__ NER_Models/ --> A user can put an ATF file and can provide the path while calling pipeline.py file

|__ sumerian_tablets/ --> setup.sh will init this directory which will store all of the .atf sumerian tablet data

```