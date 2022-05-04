import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from services import push_service as ps
from selenium.webdriver.support import expected_conditions as EC


class Crawler:

    def __init__(self):
        """
        初始必要信息
        """
        # 定义最长等待时间
        self.timeout = 180
        # # 创建Chrome浏览器配置对象实例并设定下载文件的保存目录路径
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
        # self.options.add_argument('--headless')
        # self.options.add_experimental_option("prefs", {
        #     "download.default_directory": " ",
        #     "download.prompt_for_download": False,
        #     "download.directory_upgrade": True,
        #     "safebrowsing.enabled": True
        # })
        # # 启动带有自定义设置的Chrome浏览器
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
        driver.close()

    def get_finances(self, stock_list):
        """

        :return:
        """
        driver = self.driver
        stock_statistics_list = []
        for s in stock_list:
            stock = s.split('_')[1].upper()
            url = 'https://finviz.com/quote.ashx?t={}'.format(stock)
            driver.get(url)
            time.sleep(60)
            data_i = self.wait.until(
                EC.visibility_of_all_elements_located((By.XPATH, '/html/body/div[4]/div/table[2]/tbody/tr[1]/td')))
            columns = len(data_i)
            data_j = self.wait.until(
                EC.visibility_of_all_elements_located((By.XPATH, '/html/body/div[4]/div/table[2]/tbody/tr')))
            rows = len(data_j)
            data_list = []
            data_list.append(stock)
            for c in range(1, columns + 1):
                for r in range(1, rows + 1):
                    xpath = '/html/body/div[4]/div/table[2]/tbody/tr[{}]/td[{}]'.format(r, c)
                    data = driver.find_element_by_xpath(xpath)
                    if (c % 2) == 0:
                        data_list.append(data.text)
            stock_statistics_list.append(data_list)
            ps.push_service().insert_statistics(tuple(stock_statistics_list))
        driver.close()


if __name__ == '__main__':
    Crawler().get_data()
