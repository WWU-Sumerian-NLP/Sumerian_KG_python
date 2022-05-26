from distutils import file_util
from genericpath import isfile
import unittest, os, shutil, time 

from get_cldi_data import CLDIDownloader

class TestCLDIDownloader(unittest.TestCase):
    def setUp(self):
        self.file_list = ["ur3wordlist20110805.txt", "ur3_20110805_public.atf", 
        "cdliatf_unblocked.atf", "cdli_atf_20220525.txt"]

        print("Initializing new cldi_downloader instance\n")
        os.mkdir("testing/")   
        self.cldi_downloader = CLDIDownloader(True, dest_path="testing/")
        self.cldi_downloader.download_data()
    
    def tearDown(self):
        print("tearing down cldi_downloader instance\n")
        shutil.rmtree("testing/")

    def testDownloadFolder(self):
        print("testing downloading of data\n")
        for file in self.file_list:
            self.assertEqual(True, os.path.exists("testing/" + file))
  

if __name__ == '__main__':
    unittest.main()
