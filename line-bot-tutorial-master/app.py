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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    text = event.message.text
    if text == 'レストラン予約':
        if isinstance(event.source, SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text='Hello ' + profile.display_name +'-san , you want to book a table ? \n please tell me ' ),
                    TextSendMessage(text = '何名様でお越しでしょうか？')
                    
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't use profile API without user ID"))
    elif text == '食材・弁当デリバリー':

        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=' want to oder ?'),
                TextSendMessage(text=' sorry cant not book a delivery oder rightnow !')
            ]
        )
    elif text == 'お問合せ':
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='・居酒屋「くーろん」 \n・原田商店 \n 63 Pham Viet Chanh street.,District Binh Thanh,Ho Chi Minh \n TEL：08 3840 9826 \n 携帯：090 829 5470')
            ]
        )
    elif text == 'メニュー':
        line_bot_api.reply_message(
            event.reply_token,[
                ImageSendMessage(
                        original_content_url='https://usercontent1.hubstatic.com/13821706_f520.jpg',
                        preview_image_url='https://lh3.googleusercontent.com/proxy/G12tIEnHtWQBLceysW6zYGEmi-aeJmRU_uMbAbW0vGpmMDhtEsV9dLFoIyGvgOC6jtN8397MJhzfjD_tOOa9wgEUfavGIInWJLwW8MU7anb9nbyZuO_2DMm0J_r5RZ6kEQ'
                )
            ]
        )
    elif text =='営業時間':
        line_bot_api.reply_message(
            event.reply_token,[
                TextSendMessage(text= 'asd')
            ]
        )



import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
