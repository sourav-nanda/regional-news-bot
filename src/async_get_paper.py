import os
import json
from datetime import datetime
from shutil import rmtree
import concurrent.futures
import requests
import img2pdf
from handle_editions import get_editions


# Takes around 8 seconds for download and conversion
class NewspaperDownloader:
    def __init__(self):
        os.chdir("src/storage")

        self.max_workers = 27
        self.tmp_directory = "tmp"

    def download_page(self, url, page_num):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Accept": "image/avif,image/webp,*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Alt-Used": "moapi.prameyanews.com",
            "Sec-Fetch-Dest": "image",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "cross-site",
        }

        page = requests.get(url, headers=headers)

        with open(f"tmp/{page_num}.jpg", "wb") as f:
            f.write(page.content)

    def pages_to_pdf(self, img_directory, output_pdf_path):
        if os.path.exists(output_pdf_path):
            os.remove(output_pdf_path)

        images = [
            os.path.join(img_directory, image) for image in os.listdir(img_directory)
        ]

        with open(output_pdf_path, "wb") as f:
            f.write(img2pdf.convert(images))

    def handle_directories(self):
        newspaper_path = "newspapers"

        if not os.path.exists(newspaper_path):
            os.mkdir(newspaper_path)

        os.chdir(newspaper_path)

        if os.path.exists(self.tmp_directory):
            rmtree(self.tmp_directory, ignore_errors=True)

        os.mkdir(self.tmp_directory)

    def get_page_urls(self, location):

        editions = get_editions()["editions"] # updates editions and current date, and fetches them
        edition_no = editions[location]

        data_url = f"https://moapi.prameyaepaper.com/prameya/api/master/get-image-details?image_id=&edition_id={edition_no}&customer_id=3&category={location}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.5",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
        }
        response = requests.get(data_url, headers=headers)

        data = response.json()["body"]

        pages = []

        for page in data:
            temp = json.loads(page)

            page_info = {"url": temp["image_url"], "page_num": temp["file_name"]}

            pages.append(page_info)

        current_edition_date = temp.get("edition_date",'edition_date_NA')

        pdf_name = f"{current_edition_date}__{location}.pdf"

        return pdf_name, pages

    def download_newspaper(self, location):
        pdf_name, pages = self.get_page_urls(location)

        self.handle_directories()
    
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(self.download_page, page["url"], page["page_num"])
                for page in pages
            ]
            concurrent.futures.wait(futures)

        self.pages_to_pdf("tmp", pdf_name)

        return pdf_name


if __name__ == "__main__":
    start_time = datetime.now()

    downloader = NewspaperDownloader()
    downloader.download_newspaper(location="CUTTACK")

    end_time = datetime.now()
    print(
        f'Download finished at {end_time.strftime("%H:%M:%S")} in {end_time-start_time} seconds'
    )
