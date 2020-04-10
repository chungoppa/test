from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('Vtdy706DWhhkKC9PWUH/3ch2OfTqMSAHLxGhTu5VRpfMYrREX5qPQ5Lr7GVmktzcmR6KqVpU/UW+SR8yAKDyt/PEecZg5jU9AjAIPQBvYpYNoy+bLaTLp5AjA/YJwB0Efz3OEFEuKSvxSaX6n8s0AwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('0de90a925c3ef7421376b2efbbe04ce1')

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    text = event.message.text
    if text == '1':
        if isinstance(event.source, SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text='Display name: ' + profile.display_name),
                    TextSendMessage(text='hello handsome man above ! ')
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't use profile API without user ID"))
    elif text == '2':

        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=' want to oder ?'),
                TextSendMessage(text=' sorry cant not book a delivery oder rightnow !')
            ]
        )
    elif text == '3':
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='day la so 3')
            ]
        )

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
