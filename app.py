"""LINE Messaging API echo bot example for the course project."""

import os

from dotenv import load_dotenv
from flask import Flask, abort, request
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

load_dotenv()

CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
if not CHANNEL_SECRET or not CHANNEL_ACCESS_TOKEN:
    raise RuntimeError(
        "請在 .env 設定 LINE_CHANNEL_SECRET 與 LINE_CHANNEL_ACCESS_TOKEN。"
    )

app = Flask(__name__)
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.get("/health")
def health():
    """提供不含憑證的簡易健康檢查端點。"""
    return {"status": "ok"}, 200


@app.post("/callback")
def callback():
    """驗證 LINE 簽章，再交由 SDK 分派 webhook 事件。"""
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400, description="Webhook 簽章驗證失敗。")
    return "OK", 200


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    """將收到的文字原樣回覆；replyToken 僅可短時間使用一次。"""
    with ApiClient(configuration) as api_client:
        messaging_api = MessagingApi(api_client)
        messaging_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)],
            )
        )


if __name__ == "__main__":
    # 本機開發使用；正式環境應改用具 TLS 的 WSGI 伺服器。
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")), debug=False)