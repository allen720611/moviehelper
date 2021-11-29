import os.path
import tempfile

from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError,LineBotApiError
from linebot.models import MessageEvent, TextMessage, PostbackEvent, TextSendMessage, ImagemapSendMessage, BaseSize, MessageImagemapAction, URIImagemapAction, ImagemapArea, TemplateSendMessage, ButtonsTemplate, DatetimePickerTemplateAction
from urllib.parse import parse_qsl
import datetime
from linebot.models import (
    MessageEvent,QuickReplyButton,QuickReply,VideoMessage,TextMessage, StickerMessage, StickerSendMessage, ConfirmTemplate, TemplateSendMessage, MessageAction, URIAction, LocationMessage
 )



from get_ten_pics_and_features import get_ten_pics_and_features

yc_token='6LtqwU4k493Gys589ikza9GzxWgrHjJFIcDGc21+JcMAALUjLd2xLzGRJft575QbIOeaUEedDr6QMf4mormSu0bCA8QuUTGj0kC0Im1qNsovhsMLv8tHwJjE2PkLvA44E8ckPuLRtWlTu3sNq+rNmwdB04t89/1O/w1cDnyilFU='
yu_secret='62fedcb34c8415668774fd2ccdb5d73c'

sy_token='2IT+lGbqil5lJCuY8ijAtLswcNi3sShNWPLoBOxNzo3iwm5Ob+8JyNsymS9WQCsKYp7YEhtTAIC2+C2Dm2sMvztIsDoKAaYXDUKxfh6OkpqmObF0eK2+ebunvj4IWw/OiS0eac9a6eJXp1c+y7b3wAdB04t89/1O/w1cDnyilFU='
sy_secret='d91f9849821716b3500eb7686daf3f8b'

line_bot_api = LineBotApi(sy_token)
handler = WebhookHandler(sy_secret)

@app.route("/callback", methods=['POST'])



def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'




@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    userid = event.source.user_id
    profile = line_bot_api.get_profile(str(userid))
    username=profile.display_name
    if mtext == '@圖片地圖':
        sendImgmap(event)

    elif mtext == '@日期時間':
        sendDatetime(event)

    elif mtext == '@儲存人臉特徵':
        user_camera_open(event)

    elif mtext == '@看電影評論':
        comment_show(event)

    elif mtext =='@彩蛋':
        line_bot_api.reply_message(event.reply_token,TextSendMessage('我誰~~~！'))

    elif mtext == '@id':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(userid))

    elif mtext == '@name':
        try:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(username))
        except LineBotApiError as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage('no name'))
    elif mtext == '@轉盤樣板':
        sendCarousel(event)






#儲存影片
@handler.add(MessageEvent,message=(VideoMessage))
def handle_content_message(event):
    userid = event.source.user_id
    profile = line_bot_api.get_profile(str(userid))
    username = profile.display_name
    static_tmp_path='./resources'
    # if isinstance(event.message,VideoMessage):
    #     ext='mp4'
    # else:
    #     return

    message_content=line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path,prefix=username+'___',delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path=tf.name

    dist_path=tempfile_path+'.mp4'
    dist_name=os.path.basename(dist_path)
    os.rename(tempfile_path,dist_path)

    line_bot_api.reply_message(
        event.reply_token,[
            TextSendMessage(text='成功搜集人臉特徵')
        ]


    )



@handler.add(PostbackEvent)  #PostbackTemplateAction觸發此事件

def comment_show(event):
    flex_message = TextSendMessage(text='以下有雷，請小心',
                                   quick_reply=QuickReply(items=[
                                       QuickReplyButton(action=MessageAction(label="PTT",
                                                                             text="https://www.ptt.cc/bbs/movie/index.html")),
                                       QuickReplyButton(action=MessageAction(label="DCARD",
                                                                             text="https://www.dcard.tw/f/movie")),

                                   ]))
    line_bot_api.reply_message(event.reply_token, flex_message)



def handle_postback(event):
    backdata = dict(parse_qsl(event.postback.data))  #取得data資料
    if backdata.get('action') == 'sell':
        sendData_sell(event, backdata)


def user_camera_open(event):
    queries = ConfirmTemplate(
        text="人臉註冊請錄製5秒以上的影片上傳，請問是否開啟相機?",
        actions=[
            URIAction(
                label='開啟相機',
                uri='line://nv/camera'
            ),
            MessageAction(label='不需要', text='不需要')

        ])

    temp_msg = TemplateSendMessage(alt_text='確認訊息', template=queries)

    line_bot_api.reply_message(event.reply_token, temp_msg)





def sendImgmap(event):  #圖片地圖
    try:
        image_url = 'https://i.imgur.com/Yz2yzve.jpg'  #圖片位址
        imgwidth = 1040  #原始圖片寛度一定要1040
        imgheight = 300
        message = ImagemapSendMessage(
            base_url=image_url,
            alt_text="圖片地圖範例",
            base_size=BaseSize(height=imgheight, width=imgwidth),  #圖片寬及高
            actions=[
                MessageImagemapAction(  #顯示文字訊息
                    text='你點選了紅色區塊！',
                    area=ImagemapArea(  #設定圖片範圍:左方1/4區域
                        x=0,
                        y=0,
                        width=imgwidth*0.25,
                        height=imgheight
                    )
                ),
                URIImagemapAction(  #開啟網頁
                    link_uri='http://www.e-happy.com.tw',
                    area=ImagemapArea(  #右方1/4區域(藍色1)
                        x=imgwidth*0.75,
                        y=0,
                        width=imgwidth*0.25,
                        height=imgheight
                    )
                ),
            ]
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendDatetime(event):  #日期時間
    try:
        message = TemplateSendMessage(
            alt_text='日期時間範例',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/VxVB46z.jpg',
                title='日期時間示範',
                text='請選擇：',
                actions=[
                    DatetimePickerTemplateAction(
                        label="選取日期",
                        data="action=sell&mode=date",  #觸發postback事件
                        mode="date",  #選取日期
                        initial="2020-10-01",  #顯示初始日期
                        min="2020-10-01",  #最小日期
                        max="2021-12-31"  #最大日期
                    ),
                    DatetimePickerTemplateAction(
                        label="選取時間",
                        data="action=sell&mode=time",
                        mode="time",  #選取時間
                        initial="10:00",
                        min="00:00",
                        max="23:59"
                    ),
                    DatetimePickerTemplateAction(
                        label="選取日期時間",
                        data="action=sell&mode=datetime",
                        mode="datetime",  #選取日期時間
                        initial="2020-10-01T10:00",
                        min="2020-10-01T00:00",
                        max="2021-12-31T23:59"
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendData_sell(event, backdata):  #Postback,顯示日期時間
    try:
        if backdata.get('mode') == 'date':
            dt = '日期為：' + event.postback.params.get('date')  #讀取日期
        elif backdata.get('mode') == 'time':
            dt = '時間為：' + event.postback.params.get('time')  #讀取時間
        elif backdata.get('mode') == 'datetime':
            dt = datetime.datetime.strptime(event.postback.params.get('datetime'), '%Y-%m-%dT%H:%M')  #讀取日期時間
            dt = dt.strftime('{d}%Y-%m-%d, {t}%H:%M').format(d='日期為：', t='時間為：')  #轉為字串
        message = TextSendMessage(
            text=dt
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

if __name__ == '__main__':
    app.run()
