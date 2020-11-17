import scrapy

from invest_crawler.items import InvestCrawlerItem
from selenium import webdriver
import time
from method import kiwoom_daily_report, insert_kiwoom_daily_report
from selenium.webdriver.common.keys import Keys

class investSpider(scrapy.Spider):
    # scrapy crawl invest -o test.csv  로 실행함
    name="kiwoom_daily_report"
    allowed_domains=["https://www.kiwoom.com/"]
    start_urls=["https://www.kiwoom.com/nkw.templateFrameSet.do?m=m0601010000"]

    def __init__(self):
        scrapy.Spider.__init__(self)
        # chrome드라이버 절대경로
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        # options.add_argument('window-size=1920x1080')
        # options.add_argument("disable-gpu")
        # options.add_argument("--disable-gpu")
        self.browser= webdriver.Chrome('/home/test/Downloads/chromedriver',chrome_options=options)

    def parse(self,response):
        self.browser.get(response.url)
        time.sleep(5)
        # 대기할 시간
        print("버튼 누르기 전")
        self.browser.switch_to.frame('frame1')
        self.browser.switch_to.frame('frame1')
        self.browser.switch_to.frame('cross_ifm')
        # 파일명 ( 디비에 저장하고 검사 후 중복이면 다운로드안함, 중복아니면 다운로드 )
        
        text = self.browser.find_element_by_xpath('/html/body/div[1]/table/tbody/tr[1]/td[2]/a').text
        print("dbcheck")
      
        return_valut=kiwoom_daily_report(text)
        print("dbcheck-end")
        print(return_valut)
        print("파일다운로드")
        
        if return_valut==1:
            print("동작안함")
        else:
            print("다운로드진행")
            check = self.browser.find_element_by_xpath('/html/body/div[1]/table/tbody/tr[1]/td[4]/a').click()
            insert_kiwoom_daily_report(text)
            # 디비에 저장
        time.sleep(3)
        print("종료")
        

       