from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,StickerSendMessage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium import webdriver

import time
import os



from selenium import webdriver
from linebot.models import *
import time

def web_get_address(web):
    chrome_options = webdriver.ChromeOptions()
    chromeOption.add_argument("--lang=zh-CN.UTF8")
    chromeOption.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0')
    driver = webdriver.Chrome()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--headless") #無頭模式
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    #driver = webdriver.Chrome(executable_path='/Users/poppyyang/crawlers/chromedriver', options = Options())

    driver.get(web)

    try:
        address = driver.find_element(By.CLASS_NAME, 'm6QErb .rogA2c').text
    except:
        address = '無地址提供'
    try:
        time = driver.find_element(By.CLASS_NAME, 'm6QErb .OqCZI').text.replace('營業中 ⋅ ', '')
    except:
        time = '營業中'
    driver.quit()
    return address, time


def input_wanted(search):
    address, limittime = [], []

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--headless") #無頭模式
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    # driver = webdriver.Chrome()
    # driver.set_window_size(1024, 960)

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = os.getenv('GOOGLE_CHROME_BIN',None)
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--no-sandbox')
    # driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=os.getenv('CHROMEDRIVER_PATH',None))

    # chrome_options = webdriver.ChromeOptions()
    # chromeOption.add_argument("--lang=zh-CN.UTF8")
    # chromeOption.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0')
    # driver = webdriver.Chrome()
    chromeOption = webdriver.ChromeOptions()
    chromeOption.add_argument("--lang=zh-CN.UTF8")
    chromeOption.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0')


    driver = webdriver.Chrome()
    driver.set_window_size(1024, 960)

    # driver = webdriver.Chrome(executable_path='/Users/poppyyang/crawlers/chromedriver', options = Options())
    driver.get('https://www.google.com.tw/maps/search/' + search + '/data=!4m4!2m3!5m1!2e1!6e5')
    driver.maximize_window()

    driver.implicitly_wait(2)

    # 1st info
    operation = driver.find_element(By.XPATH,
                                    '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]')

    name_type = operation.find_elements(By.CLASS_NAME, 'Nv2PK')
    websites = operation.find_elements(By.TAG_NAME, 'a')

    name = [i.text.split('\n')[0] for i in name_type]
    # comment = [i.text.split('\n')[1][:3] for i in name_type]
    # shoptype = [i.text.split('\n')[2].split()[0] for i in name_type]
    # website = [str(i.get_attribute('href')) for i in websites]
    # addr = [web_get_address(i)[0] for i in website]

    # for i in website:
    #     addr, time = web_get_address(i)
    #     address.append(addr)
    #     limittime.append(time)
    # driver.quit()

    return name
    # return name, comment, shoptype, website, address, limittime



app = Flask(__name__)

line_bot_api = LineBotApi('cBwUwzLyXqDhFhdsG/cglur32QRiBgbAi/3Xq3eby34MUg1zcQi2Ydb2/PPmtL0GbrhW84+TfO8nlWDjV2dTvCeSLrnhW0mA6efqIZ40zOlX1I7l47BrzXifLxD3pc5LEkQ7z0MtN4579ivGdoDK0QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('79a8d7930208c29ff1601c21c2683c37')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if '貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )
        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)

        return

    if msg in ['hi', 'Hi!']:
        r = 'Hi!'

    elif '高雄美食' == msg:
        name = input_wanted('高雄美食')
        r = name

    else:
        r = '抱歉！您說什麼？'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()