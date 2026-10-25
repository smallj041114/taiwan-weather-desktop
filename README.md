# 🇹🇼 台灣即時天氣查詢工具

基於 Python 與 Tkinter 開發的桌面端氣象預報查詢工具，串接中央氣象局 (CWA) OpenData API，提供全台各縣市即時天氣、氣溫、降雨機率與未來 36 小時預報查詢。

## 專案特色
- **動態選單聯動：** 支援「北部、中部、南部、東部、離島」五大區域與所屬縣市的連動下拉選單。
- **日夜圖示自適應：** 根據系統時間自動判斷日夜，自動從 CWA 抓取並快取對應的天氣圖示（PNG）。
- **多時段預報展示：** 直觀呈現未來 36 小時的氣象變化（含日期、星期、天氣狀況、降雨機率與溫差範圍）。

## 使用技術
- **程式語言：** Python
- **GUI 介面：** Tkinter, ttk
- **API 與網路請求：** Requests (串接中央氣象局 F-C0032-001 開放資料集)
- **影像處理：** Pillow (PIL) 用於圖示縮放與格式轉換
- **日期與時間：** Datetime

## 執行
1.可以先到中央氣象局的氣象資料開放平台登入取的API  https://opendata.cwa.gov.tw/index  登入並取得授權碼  
2.確保已安裝 Python 及相關依賴套件：
   ```bash
   pip install requests pillow
   ```
3.執行程式
   ```bash
   python weather.py
   ```

## 實際操作畫面
<img width="448" height="427" alt="image" src="https://github.com/user-attachments/assets/6cf2ff93-6b4b-490b-92a8-906db2e65ed9" />

介紹影片連結：https://www.youtube.com/watch?v=RmkIM0DE2Tg
