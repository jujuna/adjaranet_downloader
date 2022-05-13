import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from urllib.parse import urlparse, ParseResult, parse_qs, urlencode
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Download:

    def __init__(self, link, movie, season=0, series=0):
        self.link = link
        self.movie = movie
        self.season = season
        self.series = series.split(",")

    def url(self, ep):
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

    def download_serial(self):
        global Options
        Options = Options()
        Options.headless = True
        driver = webdriver.Chrome(options=Options)
        for i in range(len(self.series)):
            try:
                print("დაიწყო სეზონი -> {}, სერია {}".format(self.season, self.series[i]))
                name = "video_season{}_serie{}".format(self.season, self.series[i])
                url = self.url(series[i])
                driver.get(url)
                page_source = driver.page_source
                video = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='vjs_video_3_html5_api']"))).get_attribute("src")
                urllib.request.urlretrieve(video, name)
            except TypeError:
                print("ასეთი სერიალი არ არსებობს")

    def download_movie(self):
        global Options
        Options = Options()
        Options.headless = True
        driver = webdriver.Chrome(options=Options)
        try:
            print("დაიწყო სეზონი -> {}, სერია {}".format(self.season, self.series[i]))
            name = "video_season{}_serie{}".format(self.season, self.series[i])
            url = self.link
            driver.get(url)
            page_source = driver.page_source
            video = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='vjs_video_3_html5_api']"))).get_attribute("src")
            urllib.request.urlretrieve(video, name)
        except TypeError:
            print("ასეთი ფილმი")


link = input("ლინკი: ")
movie_type = str(input("არის ფილმი? (კი ან არა): "))
if movie_type == "არა":
    season = int(input("სეზონი: "))
    series = input("სერიები (გამოყავი მძიმეებით,მაგ:1,2,3): ")
    c = Download(link, movie_type, season, series)
else:
    c=Download(link, movie_type)
c.download_serial()
