# LINE Messaging API 註冊與實作教學

- 作者：黃笙誠（資管 3A，座號 39，學號 413630764）
- 出席次數：5
- 課程作品：115 學年度期中考

## 專案內容

- `main.tex`：XeLaTeX 繁體中文技術文件原始碼。
- `main.pdf`：編譯完成的教學文件（目標至少五頁）。
- `app.py`：LINE Messaging API Flask 回聲機器人範例。
- `requirements.txt`：Python 相依套件。
- `.env.example`：環境變數範本，請勿填入或提交真實憑證。

## 編譯文件

在已安裝 XeLaTeX 與繁體中文字型的環境中，於本目錄執行兩次 `xelatex -interaction=nonstopmode -halt-on-error main.tex`，讓目錄及交互參照更新。

## 執行範例程式

1. 建立虛擬環境並安裝 `requirements.txt`。
2. 複製 `.env.example` 為 `.env`，填入 LINE Developers Console 的 Channel Secret 與 Channel Access Token。
3. 執行 `python app.py`，以瀏覽器確認 `/health` 回傳 `{"status":"ok"}`。
4. 將公開 HTTPS 網址的 `/callback` 設為 Messaging API 的 Webhook URL，啟用 Use webhook 並執行 Verify。
5. 以 LINE 帳號加入官方帳號好友，傳送文字測試回聲回覆。

真實 token、secret 與 `.env` 不應加入版本控制或分享。正式服務請使用 HTTPS、關閉除錯模式並配置適當的 WSGI 伺服器。