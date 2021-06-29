# -*- coding:utf-8 -*-
# @Author:huan
# @Time  :2021-06-10
import time
import os
from selenium import webdriver
from common.read_data import read
from common.log_handler import log
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pathlib import Path

# 获取cfg.ini配置文件
data = read.load_ini("configs\cfg.ini")

img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")


class Driver:
    """浏览器驱动类"""
    _driver = None

    @classmethod
    def get_driver(cls, browser_name="Chrome"):
        """
        获取浏览器驱动对象，若第一次进入此函数则创建并返回；第二次以后进入则直接返回（之前已创建好的）
        :param browser_name: 浏览器驱动对象
        :return:
        """
        if cls._driver is None:
            if browser_name == "Chrome":
                cls._driver = webdriver.Chrome()
            elif browser_name == "Firefox":
                cls._driver = webdriver.Firefox()
            else:
                raise ("没有找到此类型的浏览器，请检查传入的参数", browser_name)

            cls._driver.maximize_window()
            cls._driver.implicitly_wait(data["time"]["implicitly_wait"])
            # cls._driver.get(data["poll"]["url"])
            # cls.login()

        return cls._driver

    # @classmethod
    # def login(cls):
    #     cls._driver.find_element_by_id("username").send_keys(data["poll"]["username"])
    #     cls._driver.find_element_by_id("password").send_keys(data["poll"]["password"])
    #     cls._driver.find_element_by_id("btnLogin").click()


class CommBase(Driver):

    # 初始化
    def __init__(self):
        self.driver = Driver.get_driver()

    # 打开url
    def get_url(self, url):
        self.driver.get(url)

    # 关闭当前窗口
    def close_driver(self):
        self.driver.close()

    # 退出浏览器
    def quit(self):
        self.driver.quit()

    # 刷新当前页面
    def refresh(self):
        self.driver.refresh()

    # 查找元素-单个
    def find_element(self, locator, n=99):
        try:
            if n == 99:
                element = self.driver.find_element(locator)
                self.__highlight(element)
                return element
            else:
                element = self.driver.find_elements(*locator)[n]
                self.__highlight(element)
                return element
        except Exception as e:
            log.error(f"{locator}元素未找到 \n", e)
            self.save_img("未找到元素")

    # 查找元素-多个
    def find_elements(self, locator):
        try:
            elements = self.driver.find_elements(locator)
            self.__highlight(elements)
            return elements
        except Exception as e:
            log.error(f"{locator}元素未找到 \n", e)
            self.save_img("未找到元素")

    # 等待元素可见
    def wait_ele_visible(self,
                         locator,
                         timeout=data["time"]["test_out"],
                         poll_frequency=data["time"]["poll_time"]):
        """
        等待元素可见，显示等待
        :param locator: 定位的元素，形式为元组格式的，如(By.ID,"kw")
        :param timeout: 最长等待时间
        :param poll_frequency: 轮询周期
        :return:
        """
        try:
            element = WebDriverWait(
                driver=self.driver,  # 浏览器驱动对象
                timeout=timeout,  # 超时时间
                poll_frequency=poll_frequency  # 轮询时间
            ).until(EC.visibility_of_element_located(locator))
            self.__highlight(element)
            return element
        except Exception as e:
            log.error(f"等待元素{locator}可见失败！ \n", e)
            self.save_img("等待元素可见失败")

    def wait_ele_clickable(self,
                           locator,
                           timeout=data["time"]["test_out"],
                           poll_frequency=data["time"]["poll_time"]):
        """
        判断某个元素中是否可见并且是enable的，代表可点击
        """
        try:
            element = WebDriverWait(
                driver=self.driver,  # 浏览器驱动对象
                timeout=timeout,  # 超时时间
                poll_frequency=poll_frequency  # 轮询时间
            ).until(EC.element_to_be_clickable(locator))
            self.__highlight(element)
            return element
        except Exception as e:
            log.error(f"元素{locator}可点击失败 \n", e)
            self.save_img("等待可点击失败")

    def wait_ele_presence(self,
                          locator,
                          timeout=data["time"]["test_out"],
                          poll_frequency=data["time"]["poll_time"]):
        """
        等待元素存在
        """
        try:
            element = WebDriverWait(
                driver=self.driver,  # 浏览器驱动对象
                timeout=timeout,  # 超时时间
                poll_frequency=poll_frequency  # 轮询时间
            ).until(EC.presence_of_element_located(locator))
            self.__highlight(element)
            return element
        except Exception as e:
            log.info(f"等待元素{locator}存在失败！\n", e)
            self.save_img(f"等待存在失败")

    # 等待元素不存在或者不存在，可见就返回false（一般用于等待类似页面初始loading的消失）
    def wait_ele_invisibility(self,
                              locator,
                              timeout=data["time"]["test_out"],
                              poll_frequency=data["time"]["poll_time"],
                              doc=''):
        try:
            message = 'Element: {0} is visible in {1} seconds.'.format(locator, timeout)
            WebDriverWait(
                driver=self.driver,  # 浏览器驱动对象
                timeout=timeout,  # 超时时间
                poll_frequency=poll_frequency  # 轮询时间
            ).until(EC.presence_of_element_located(locator), message)
        except:
            log.info('{}失败！'.format(doc))
            raise

    # 判断指定的元素中是否包含了预期的字符串
    def wait_ele_text_present(self,
                              locator,
                              text,
                              timeout=data["time"]["test_out"],
                              poll_frequency=data["time"]["poll_time"]):
        try:
            element = WebDriverWait(
                driver=self.driver,  # 浏览器驱动对象
                timeout=timeout,  # 超时时间
                poll_frequency=poll_frequency  # 轮询时间
            ).until(EC.text_to_be_present_in_element(locator, text))
            self.__highlight(element)
            return element
        except Exception as e:
            log.info('判断元素{}中包含{}失败！'.format(locator, text))
            raise e

    # 判断页面上是否存在alert
    def wait_alert(self,
                   timeout=data["time"]["test_out"],
                   poll_frequency=data["time"]["poll_time"]):
        try:
            WebDriverWait(
                driver=self.driver,  # 浏览器驱动对象
                timeout=timeout,  # 超时时间
                poll_frequency=poll_frequency  # 轮询时间
            ).until(EC.alert_is_present())
        except Exception as e:
            message = 'Alert Element: cannot be found in {0} seconds.'.format(timeout)
            log.info(message)
            raise e

    # 保留截图
    def save_img(self, name):
        if not os.path.exists(img_path):
            log.info(f"{img_path} not exists, create it.")
            os.mkdir(img_path)
            now_time = time.strftime("%Y%m%d%H%M%S")
            file_name = os.path.join(img_path, name + "_" + str(now_time) + ".png")
            self.driver.get_screenshot_as_file(file_name)
            log.info(f"截取网页成功。文件名称为：{file_name}")

    #点击操作
    def click(self, locator, n=99):
        element = self.find_element(locator, n)
        if element.is_enabled():
            try:
                element.click()
            except Exception as e:
                log.error(f"点击元素{locator}失败!")
                self.save_img("点击失败")
                raise e

    #查找元素后清除默认文本内容
    def clear(self, locator):
        try:
            return self.driver.find_element(*locator).clear()
        except Exception as e:
            log.error(f"清除元素{locator}的默认文本失败!")
            raise e

    #输入操作
    def send_keys(self, locator, text, n=99):
        element = self.find_element(locator, n)
        element.clear()
        try:
            element.send_keys(text)
        except Exception as e:
            log.error(f"在元素{locator}输入内容失败!")
            self.save_img("输入失败")
            raise e

    #获取元素文本内容
    def text(self, locator, n=99):
        element = self.find_element(locator, n)
        try:
            return element.text
        except Exception as e:
            log.error(f"获取元素{locator}的文本内容失败!")
            raise e


    # 元素高亮
    def __highlight(self, element):
        self.driver.execute_script("arguments[0].setAttribute('style',argument[1]);", element, "border: 2px solid red;")
