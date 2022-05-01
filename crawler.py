import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from services import push_service as ps


class Crawler:

    def __init__(self):
        """
        初始必要信息
        """
        # 定义最长等待时间
        self.timeout = 60
        # 创建Chrome浏览器配置对象实例并设定下载文件的保存目录路径
        self.options = Options()
        # 解决DevToolsActivePort文件不存在的报错
        self.options.add_argument('--no-sandbox')
        # 设置浏览器分辨率
        self.options.add_argument('window-size=1920x3000')
        # 谷歌文档提到需要加上这个属性来规避bug
        self.options.add_argument('--disable-gpu')
        # 隐藏滚动条，应对一些特殊页面
        self.options.add_argument('--hide-scrollbars')
        # 不加载图片，提升运行速度
        self.options.add_argument('blink-settings=imagesEnabled=false')
        self.options.add_argument('--headless')
        self.options.add_experimental_option("prefs", {
            "download.default_directory": " ",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        # 启动带有自定义设置的Chrome浏览器
        self.driver = webdriver.Chrome('C:/Users\zj100\Downloads\chromedriver_win32\chromedriver.exe',
                                       options=self.options)
        self.driver.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.driver, self.timeout)

    def get_data(self):
        """
        :return:
        """
        driver = self.driver
        url = 'https://finance.sina.com.cn/stock/usstock/'
        # 获取网页
        driver.get(url)
        news = self.driver.find_elements_by_xpath('/html/body/div[8]/div[1]/div[1]/div[2]/ul/li/a')
        news_list = []
        for n in news:
            n_list = []
            title = n.text
            link = n.get_attribute('href')
            busi_date = datetime.datetime.now().strftime("%Y%m%d")
            n_list.append(busi_date)
            n_list.append(title)
            n_list.append(link)
            news_list.append(n_list)
        ps.push_service().insert_news(tuple(news_list))
