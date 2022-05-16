import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from urllib.parse import urlparse, ParseResult, parse_qs, urlencode
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def IsMovie(link):
    url = link
    url, sharp, frag = url.partition('#')
    base, q, query = url.partition('?')
    query_dict = parse_qs(query)
    if 'season' in query_dict:
        return 0
    else:
        return 1
    

class Configuration:
    global Options
    Options = Options()
    Options.headless = True
    Options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=Options)


class Download:

    def __init__(self, link, movie, season=0, series=0):
        self.link = link
        self.movie = movie
        self.season = season
        self.series = series.split(",") if series else series


    def main(self):
        if self.movie:
            self.download_serial()
        else:
            self.download_movie()

    def url(self, ep=0):
        url = self.link
        param, newvalue, param2, newvalue2 = 'season', self.season, 'episode', ep

        url, sharp, frag = url.partition('#')
        base, q, query = url.partition('?')
        query_dict = parse_qs(query)
        query_dict[param][0] = newvalue
        query_dict[param2][0] = newvalue2
        query_new = urlencode(query_dict, doseq=True)
        url_new = f'{base}{q}{query_new}{sharp}{frag}'
        return url_new

    def info(self, ep=0):
        driver = Configuration.driver
        if self.movie:
            driver.get(self.url(ep))
        else:
            driver.get(self.link)
        video = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='vjs_video_3_html5_api']"))).get_attribute("src")
        name = driver.find_element(By.XPATH, '/html/body/main/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[1]').text
        name = f'{name} -> season {self.season} ep {ep}' if self.movie else f'{name}'
        data = {"name": name, "video": video}
        return data

    def download_serial(self):
        for i in self.series:
            try:
                data = self.info(i)
                print(f"დაიწყო {data['name']} გადმოწერა")
                urllib.request.urlretrieve(data['video'], data['name'])
            except TypeError:
                print("ასეთი სერიალი არ არსებობს")

    def download_movie(self):
        try:
            data = self.info()
            print(f"დაიწყო {data['name']} გადმოწერა")
            urllib.request.urlretrieve(data['video'], data['name'])
        except TypeError:
            print("ასეთი ფილმი არ არსებობს")


link = input("ლინკი: ")
if IsMovie(link):
    c = Download(link, 0).main()
else:
    season = int(input("სეზონი: "))
    series = input("სერიები (გამოყავი მძიმეებით,მაგ:1,2,3): ")
    c = Download(link, 1, season, series).main()
