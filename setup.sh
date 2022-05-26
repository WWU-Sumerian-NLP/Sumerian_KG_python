#get CLDI Data
cd Data_Collection/CLDI_DOWNLOADER
sh download_cldi_data.sh 

cd ..
cd .. 

#get NER models
cd NER_Models/
sh setup_models.sh