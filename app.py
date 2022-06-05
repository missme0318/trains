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

line_bot_api = LineBotApi('GRterwMoZSwbiBY2BELd2tHouSCaJK4qZnMhDQoJCS8reJ8ncOle1DXwIh6+DtJrEKvRSPmo5V/Q7a8jw7yw7BRlJ6m6sR6KH/7tR1B7/qc9+ca3gOJt5i8MkJfCz/HhMaCxBf1wDXgqRkNfNniD2AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e012b30c4d16f4fb248e72e75f98d456')


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