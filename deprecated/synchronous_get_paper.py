import requests
from datetime import datetime
import os
from shutil import rmtree
from PIL import Image

class NewspaperDownloader:

    def __init__(self, location='SAMBALPUR'):

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
        self.newspaper_path = 'newspapers'
        self.tmp_directory = 'tmp'
        self.STATUS = self.INITIAL_STATUS = 200
        
        
        self.location = location
        self.edition_no = self.editions[self.location]
        os.chdir(self.newspaper_path)

    def images_to_pdf(self,image_paths, output_pdf_path, resolution=100.0):
 
        images = [Image.open(image_path) for image_path in image_paths]
        images[0].save(output_pdf_path,"PDF",resolution=resolution,save_all=True,append_images=images[1:])

    def download_newspaper(self):
        today = datetime.now()
        
        if os.path.exists(self.tmp_directory):
            rmtree(self.tmp_directory, ignore_errors=True)

        os.mkdir(self.tmp_directory)
    

        while self.STATUS == 200:
            page_no = f'0{self.page_index}' if self.page_index < 10 else str(self.page_index)

            url = f"https://moapi.prameyanews.com/prameya/document/pdf/3_102_{self.edition_no}_{today.strftime('%Y%m%d')}_00{page_no}.jpg"

            page = requests.get(url, headers=self.headers)

            self.STATUS = page.status_code
            self.page_index += 1

            if self.STATUS == 200:
                with open(f'tmp/{page_no}.jpg', 'wb') as f:
                    f.write(page.content)
            else:
                break

        images=[os.path.join(self.tmp_directory,image) for image in os.listdir(self.tmp_directory)]
        pdf_name=f'{today.strftime("%Y_%m_%d")}.pdf'
        
        self.images_to_pdf(images,pdf_name)

        rmtree('tmp', ignore_errors=True)
            
        print(f'Newspaper downloaded for {datetime.now().strftime("%Y-%m-%d at %H:%M:%S")}')

# if __name__ == "__main__":
downloader = NewspaperDownloader(edition_city='CUTTACK')

downloader.download_newspaper()