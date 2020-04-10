from flask import Flask, request, abort
import json
import datetime

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
    if text == '1':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerAction(label='datetime',
                                                            data='datetime_postback',
                                                            mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerAction(label='date',
                                                            data='date_postback',
                                                            mode='time'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == '2':
        confirm_template = ConfirmTemplate(text='Do it?', actions=[
            MessageAction(label='Yes', text='Yes!'),
            MessageAction(label='No', text='No!'),
        ])
        template_message = TemplateSendMessage(
            alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    if text == 'レストラン予約':
        if isinstance(event.source, SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)

            image_carousel_template = ImageCarouselTemplate(columns=[
                ImageCarouselColumn(
                    image_url='https://www.clipartly.com/wp-content/uploads/2018/10/Cartoon-Alarm-Clock-Clipart-Png.png',
                    action=DatetimePickerAction(label='time',
                                                data='time_postback',
                                                mode='time')),
            ])
            template_message = TemplateSendMessage(
                alt_text='ImageCarousel alt text', template=image_carousel_template)
            line_bot_api.reply_message(event.reply_token, template_message)
            
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='Hello  ' + profile.display_name + '-san :) , you want to book a table ? \n please tell me'),
                    TextSendMessage(text='何名様でお越しでしょうか？', quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=PostbackAction(label="label1", data="data1")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="label2", text="text2")
                        ),
                        QuickReplyButton(
                            action=DatetimePickerAction(label="label3",
                                                        data="data3",
                                                        mode="date")
                        ),
                        QuickReplyButton(
                            action=CameraAction(label="label4")
                        ),
                        QuickReplyButton(
                            action=CameraRollAction(label="label5")
                        ),
                        QuickReplyButton(
                            action=LocationAction(label="label6")
                        ),
                    ]))
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
                TextSendMessage(text=' sorry  delivery oder is not avalable rightnow !')
            ]
        )
    elif text == 'お問合せ':
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(
                    text='・居酒屋「くーろん」 \n・原田商店 \n 63 Pham Viet Chanh street.,District Binh Thanh,Ho Chi Minh \n TEL：08 3840 9826 \n 携帯：090 829 5470')
            ]
        )
    elif text == 'メニュー':
        line_bot_api.reply_message(
            event.reply_token, [
                ImageSendMessage(
                    original_content_url='https://lh3.googleusercontent.com/proxy/G12tIEnHtWQBLceysW6zYGEmi-aeJmRU_uMbAbW0vGpmMDhtEsV9dLFoIyGvgOC6jtN8397MJhzfjD_tOOa9wgEUfavGIInWJLwW8MU7anb9nbyZuO_2DMm0J_r5RZ6kEQ',
                    preview_image_url='https://lh3.googleusercontent.com/proxy/G12tIEnHtWQBLceysW6zYGEmi-aeJmRU_uMbAbW0vGpmMDhtEsV9dLFoIyGvgOC6jtN8397MJhzfjD_tOOa9wgEUfavGIInWJLwW8MU7anb9nbyZuO_2DMm0J_r5RZ6kEQ'
                )
            ]
        )
    elif text == '営業時間':
        bubble_string = """
                {
                  "type": "bubble",
                  "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "image",
                        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Sushi_platter.jpg/1200px-Sushi_platter.jpg",
                        "position": "relative",
                        "size": "full",
                        "aspectMode": "cover",
                        "aspectRatio": "1:1",
                        "gravity": "center"
                      },
                      {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                          {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                              {
                                "type": "text",
                                "text": "Sushi",
                                "weight": "bold",
                                "size": "xl",
                                "color": "#ffffff"
                              },
                              {
                                "type": "box",
                                "layout": "baseline",
                                "margin": "md",
                                "contents": [
                                  {
                                    "type": "icon",
                                    "size": "sm",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                  },
                                  {
                                    "type": "icon",
                                    "size": "sm",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                  },
                                  {
                                    "type": "icon",
                                    "size": "sm",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                  },
                                  {
                                    "type": "icon",
                                    "size": "sm",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                  },
                                  {
                                    "type": "icon",
                                    "size": "sm",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
                                  },
                                  {
                                    "type": "text",
                                    "text": "4.0",
                                    "size": "sm",
                                    "color": "#d6d6d6",
                                    "margin": "md",
                                    "flex": 0
                                  }
                                ]
                              }
                            ]
                          },
                          {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                              {
                                "type": "text",
                                "text": "¥62,000",
                                "color": "#a9a9a9",
                                "decoration": "line-through",
                                "align": "end"
                              },
                              {
                                "type": "text",
                                "text": "¥42,000",
                                "color": "#ebebeb",
                                "size": "xl",
                                "align": "end"
                              }
                            ]
                          }
                        ],
                        "position": "absolute",
                        "offsetBottom": "0px",
                        "offsetStart": "0px",
                        "offsetEnd": "0px",
                        "backgroundColor": "#00000099",
                        "paddingAll": "20px"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "text",
                            "text": "OFF - 20 %",
                            "color": "#ffffff"
                          }
                        ],
                        "position": "absolute",
                        "backgroundColor": "#ff2600",
                        "cornerRadius": "20px",
                        "paddingAll": "5px",
                        "offsetTop": "10px",
                        "offsetEnd": "10px",
                        "paddingStart": "10px",
                        "paddingEnd": "10px"
                      }
                    ],
                    "paddingAll": "0px"
                  }
                }
                """
        message = FlexSendMessage(alt_text="hello", contents=json.loads(bubble_string))
        line_bot_api.reply_message(
            event.reply_token,
            message
        )


import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
