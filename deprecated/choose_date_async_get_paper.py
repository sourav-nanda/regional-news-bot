import requests
from datetime import datetime
import os
from shutil import rmtree
import img2pdf
import concurrent.futures

class NewspaperDownloader:

    def __init__(self, location='SAMBALPUR', today=datetime.now().strftime('%Y%m%d')):

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Accept": "image/avif,image/webp,*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Alt-Used": "moapi.prameyanews.com",
            "Sec-Fetch-Dest": "image",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "cross-site"
        }

        self.editions={'BHUBANESWAR': 4931, 'KHORDA': 4928, 'ANGUL': 4920, 'BALASORE': 4921, 'CUTTACK': 4930, 
                       'PANIKOILI': 4922, 'JEYPORE': 4917, 'KBK': 4924, 'KENDRAPADA': 4927, 'KENDUJHAR': 4919, 
                       'MAYURBHANJ': 4918, 'PURI': 4929, 'ROURKELA': 4923, 'SAMBALPUR': 4925, 'BERHAMPUR': 4926, 
                       'RABIBAR': 4856}

        self.page_index = 1
        self.STATUS = self.INITIAL_STATUS = 200
        self.today=today

        self.location = location
        self.edition_no = self.editions[self.location]
        self.pdf_name = f"{self.today} - {self.location}.pdf" if self.location != 'RABIBAR' else 'RABIBAR.pdf'
        
    
        self.data_url=f'https://moapi.prameyaepaper.com/prameya/api/master/get-image-details?image_id=&edition_id={self.edition_no}&customer_id=3&category={self.location}'
        self.response=requests.get(self.data_url, headers=self.headers)
        self.num_pages= len(self.response.json()['body'])

        self.page_names= [f'0{page_index}' if page_index < 10 else str(page_index) for page_index in range(1,self.num_pages)]
        self.pages = [f"https://moapi.prameyanews.com/prameya/document/pdf/3_102_{self.edition_no}_{self.today}_00{page_name}.jpg" for page_name in self.page_names]
        
    def images_to_pdf(self, img_directory, output_pdf_path):

        if os.path.exists(output_pdf_path):
            os.remove(output_pdf_path)

        images = [os.path.join(img_directory, image) for image in os.listdir(img_directory)]

        with open(output_pdf_path, "wb") as f:
            f.write(img2pdf.convert(images))

    def handle_directory(self):

        tmp_directory = 'tmp'
        newspaper_path = 'newspapers'

        if not os.path.exists(newspaper_path):
            os.mkdir(newspaper_path)

        os.chdir(newspaper_path)

        if os.path.exists(tmp_directory):
            rmtree(tmp_directory, ignore_errors=True)

        os.mkdir(tmp_directory)

    
    def download_newspaper_page(self,url,page_num):
        
        page = requests.get(url, headers=self.headers)
        
        with open(f'tmp/{page_num}.jpg', 'wb') as f:
            f.write(page.content)

    def download_newspaper(self):

        start_time=datetime.now()

        self.handle_directory()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=9) as executor:
            futures = [executor.submit(self.download_newspaper_page, page, page_name) for page,page_name in zip(self.pages,self.page_names)]
            concurrent.futures.wait(futures)

        self.images_to_pdf('tmp', self.pdf_name)

        end_time=datetime.now()
        
        print(
            f'Download finished at {end_time.strftime("%H:%M:%S")} in {end_time-start_time} seconds'
        )

downloader = NewspaperDownloader(location='SAMBALPUR')
downloader.download_newspaper()