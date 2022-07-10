from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,StickerSendMessage
)

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
    elif '聊天' in msg:
        r = '我是機器人'
    else:
        r = '抱歉！您說什麼？'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()