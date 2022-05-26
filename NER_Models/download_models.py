from io import BytesIO
import urllib, h5py
import pandas as pd 
from urllib import request



class ModelDownloader:
    def __init__(self):
        self.bi_lstm_crf_url = "https://github.com/cdli-gh/Sumerian-Translation-Pipeline/blob/master/Saved_Models/NER/NER_Bi_LSTM_CRF.h5?raw=true"
        self.bi_lstm_url = "https://github.com/cdli-gh/Sumerian-Translation-Pipeline/blob/master/Saved_Models/NER/NER_Bi_LSTM.h5?raw=true" 
        self.crf_url = "https://github.com/cdli-gh/Sumerian-Translation-Pipeline/blob/master/Saved_Models/NER/NER_CRF.pkl?raw=true"

    def download_all_models(self):
        all_urls = [self.bi_lstm_crf_url, self.bi_lstm_url, self.crf_url]
        for url in all_urls:
            self.download_models(url) 
        

    def download_models(self, url):
        r = request.urlopen(url)
        file_name = url.split('/')[-1][0:-9]
        print("Downloading {} model ...".format(file_name))

        result = r.read()
        with open(file_name, 'wb') as f: 
            f.write(result)

if __name__ == "__main__":
    downloader = ModelDownloader()
    downloader.download_all_models()
