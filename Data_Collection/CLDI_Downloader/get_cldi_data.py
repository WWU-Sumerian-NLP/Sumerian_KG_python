from io import BytesIO
from re import sub
import requests, zipfile, os, shutil
import gdown

class CLDIDownloader:
    def __init__(self, override_flag=False, dest_path = "../../../sumerian_tablets/"):
        self.dest_path = dest_path
        self.base_url = "https://cdli.ucla.edu/downloads"
        self.gdrive_map = {'cdli_atf_20220525.txt': "https://drive.google.com/uc?id=10_7gJyFikImUfZQqWJonV2WoQrJAiwZN", "cdli_result_20220525.txt": "https://drive.google.com/uc?id=1UkGJMhsjEnbv9N3Q9ROXS1M3PM5rAlMp"}
        self.transliterations_url = "https://cdli.ucla.edu/tools/cdlifiles/cdliatf_unblocked.zip"
        # self.urr3_sign_list_url = "https://cdli.ucla.edu/tools/cdlifiles/signlists/ur3signlisttxt.zip"
        self.urr3_word_list_url = "https://cdli.ucla.edu/tools/cdlifiles/ur3wordlisttxt.zip"
        self.urr3_transliterations_url = "https://cdli.ucla.edu/tools/cdlifiles/cdli_ur3atf.zip"
       
        self.override_flag = override_flag
    
    def download_data(self, transliterations_flag=False,
                    urr3_sign_flag=False, urr3_word_list_flag=False, urr3_transliteration_flag=False):

        if self.override_flag or transliterations_flag:
            self.download_file_from_url(self.transliterations_url)

        # if self.override_flag or urr3_sign_flag:
        #     self.download_from_url(self.urr3_sign_list_url)

        if self.override_flag or urr3_word_list_flag:
            self.download_file_from_url(self.urr3_word_list_url)

        if self.override_flag or urr3_transliteration_flag:
            self.download_file_from_url(self.urr3_transliterations_url) 

        self.download_from_gdrive()

    def download_file_from_url(self, url):
        if self.override_flag: 
            r = requests.get(url) 
            if r.status_code != 200:
                return print("Skipping: request for {} has status code: {}".format(url, r.status_code))

            file_name = url.split('/')[-1]
            if not str(file_name[-4:]) == '.zip':
                return ("Skipping: {} is not a zip file".format(file_name))
                
            print("Downloading {} ...".format(url))
            zip_file = zipfile.ZipFile(BytesIO(r.content))
            zip_file_des = os.path.join(self.dest_path, file_name)
            zip_file.extractall(zip_file_des)
            zip_file.close()
            self.clean_directory(zip_file_des)

    def download_from_gdrive(self):
        zip_file_des = os.path.join(self.dest_path, "urr3_drehem_data.zip")
        for file, url in self.gdrive_map.items():
            output = os.path.join(self.dest_path, file)
            gdown.download(url, output, quiet=False)
            with zipfile.ZipFile(output, "r") as file:
                file.extractall(zip_file_des)
            file.close()
            self.clean_directory(zip_file_des)

    def clean_directory(self, zip_file_des):
        unzip_file_list = [x for x in os.listdir(zip_file_des) if x.endswith(".atf") or x.endswith(".txt")]
        if len(unzip_file_list) < 1:
            return("ERROR: {} directory does not contain .atf or .txt files".format(zip_file_des))
        
        for unzip_file in unzip_file_list:
            shutil.move(os.path.join(zip_file_des, unzip_file),  os.path.join(self.dest_path, unzip_file)) 
            if os.path.isdir(zip_file_des):
                shutil.rmtree(zip_file_des)
            else:
                return("ERROR: {} directory not found".format(zip_file_des))


if __name__ == '__main__':
    cldi_downloader = CLDIDownloader(True)
    cldi_downloader.download_data()
