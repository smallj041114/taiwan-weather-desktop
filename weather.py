import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import datetime
import os

API_KEY = "CWA-395C9478-BD5C-460D-838E-835A91AEAC90"

region_map = {
    "北部": ["臺北市", "新北市", "基隆市", "桃園市", "新竹市", "新竹縣", "宜蘭縣"],
    "中部": ["臺中市", "苗栗縣", "彰化縣", "南投縣", "雲林縣"],
    "南部": ["高雄市", "臺南市", "嘉義市", "嘉義縣", "屏東縣"],
    "東部": ["花蓮縣", "臺東縣"],
    "離島": ["澎湖縣", "金門縣", "連江縣"]
}

ICON_DIR = "weather_icons_png"
os.makedirs(ICON_DIR, exist_ok=True)

def is_daytime():
    now = datetime.datetime.now()
    return 6 <= now.hour < 18

def fetch_weather(location_name):
    url = (
        "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
        f"?Authorization={API_KEY}&locationName={location_name}"
    )
    try:
        res = requests.get(url)
        data = res.json()

        location = data["records"]["location"][0]
        weather_elements = location["weatherElement"]

        wx = weather_elements[0]["time"][0]["parameter"]["parameterName"]
        wx_code = weather_elements[0]["time"][0]["parameter"]["parameterValue"]
        pop = weather_elements[1]["time"][0]["parameter"]["parameterName"]
        minT = weather_elements[2]["time"][0]["parameter"]["parameterName"]
        maxT = weather_elements[4]["time"][0]["parameter"]["parameterName"]
        start_time = weather_elements[0]["time"][0]["startTime"]

        return {
            "天氣": wx,
            "天氣代碼": wx_code,
            "降雨機率": pop + "%",
            "氣溫": f"{minT}°C ~ {maxT}°C",
            "時間": start_time
        }
    except Exception as e:
        return {"error": str(e)}

def download_icon(wx_code, daytime=True):
    code_str = str(wx_code).zfill(2)
    daynight = "day" if daytime else "night"
    url = f"https://www.cwa.gov.tw/V8/assets/img/weather_icons/weathers/png_icon/{daynight}/{code_str}.png"
    local_path = os.path.join(ICON_DIR, f"{daynight}_{code_str}.png")

    if not os.path.exists(local_path):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                with open(local_path, "wb") as f:
                    f.write(r.content)
            else:
                print(f"無法下載圖示，HTTP狀態碼: {r.status_code}")
                return None
        except Exception as e:
            print(f"下載圖示失敗: {e}")
            return None
    return local_path

def update_city_options(event):
    region = region_var.get()
    cities = region_map.get(region, [])
    city_combo['values'] = cities
    if cities:
        location_var.set(cities[0])
        update_weather()

def update_weather(*args):
    location = location_var.get()
    weather = fetch_weather(location)

    for widget in forecast_frame.winfo_children():
        widget.destroy()

    if "error" in weather:
        weather_label.config(text=f"資料讀取錯誤：{weather['error']}")
        temp_label.config(text="")
        rain_label.config(text="")
        time_label.config(text="")
        icon_label.config(image="")
        icon_label.image = None
    else:
        weather_label.config(text=f"天氣：{weather['天氣']}")
        temp_label.config(text=f"氣溫：{weather['氣溫']}")
        rain_label.config(text=f"降雨機率：{weather['降雨機率']}")

        dt = datetime.datetime.strptime(weather['時間'], "%Y-%m-%d %H:%M:%S")
        weekday = ["一", "二", "三", "四", "五", "六", "日"]
        if 0 <= dt.hour < 6:
            period = "凌晨"
        elif 6 <= dt.hour < 18:
            period = "白天"
        else:
            period = "晚上"

        week_str = f"週{weekday[dt.weekday()]}{period}"
        time_label.config(text=f"資料時間：{dt.strftime('%m/%d %H:%M')}（{week_str}）")

        daytime = is_daytime()
        icon_path = download_icon(weather["天氣代碼"], daytime)
        if icon_path:
            img = Image.open(icon_path)
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            icon_label.config(image=photo)
            icon_label.image = photo
        else:
            icon_label.config(image="")
            icon_label.image = None

        try:
            res = requests.get(
                f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={API_KEY}&locationName={location}"
            )
            data = res.json()
            location_data = data["records"]["location"][0]["weatherElement"]

            for i in range(3):
                start_time = location_data[0]["time"][i]["startTime"]
                wx = location_data[0]["time"][i]["parameter"]["parameterName"]
                wx_code = location_data[0]["time"][i]["parameter"]["parameterValue"]
                pop = location_data[1]["time"][i]["parameter"]["parameterName"]
                minT = location_data[2]["time"][i]["parameter"]["parameterName"]
                maxT = location_data[4]["time"][i]["parameter"]["parameterName"]

                dt = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                day_str = dt.strftime("%m/%d")
                weekday = ["一", "二", "三", "四", "五", "六", "日"]
                if 0 <= dt.hour < 6:
                    period = "凌晨"
                elif 6 <= dt.hour < 18:
                    period = "白天"
                else:
                    period = "晚上"
                    
                week_str = f"週{weekday[dt.weekday()]}{period}"

                date_label = tk.Label(forecast_frame, text=f"{day_str}\n{week_str}", font=("Arial", 10, "bold"))
                date_label.grid(row=0, column=i, padx=10)

                icon_path = download_icon(wx_code, 6 <= dt.hour < 18)
                if icon_path:
                    img = Image.open(icon_path)
                    img = img.resize((50, 50), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    icon = tk.Label(forecast_frame, image=photo)
                    icon.image = photo
                    icon.grid(row=1, column=i, padx=10)

                info = f"{wx}\n降雨：{pop}%\n{minT}~{maxT}°C"
                info_label = tk.Label(forecast_frame, text=info, font=("Microsoft JhengHei", 9), width=15, justify="center")
                info_label.grid(row=2, column=i, padx=10)

        except Exception as e:
            print("取得36小時預報失敗：", e)

def update_system_time():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    system_time_label.config(text=f"系統時間：{now}")
    root.after(1000, update_system_time)

root = tk.Tk()
root.title("台灣即時天氣查詢（CWA API）")
root.geometry("450x400")

region_var = tk.StringVar()
location_var = tk.StringVar()

region_combo = ttk.Combobox(root, textvariable=region_var, values=list(region_map.keys()), state="readonly")
region_combo.current(0)
#region_combo.set("請選擇區域")
region_combo.bind("<<ComboboxSelected>>", update_city_options)
region_combo.grid(row=0, column=0, padx=10, pady=10)

city_combo = ttk.Combobox(root, textvariable=location_var, state="readonly")
city_combo.bind("<<ComboboxSelected>>", update_weather)
city_combo.grid(row=0, column=1, padx=10, pady=10)

weather_label = tk.Label(root, text="天氣：", font=("Microsoft JhengHei", 12))
weather_label.grid(row=1, column=0, sticky="w", padx=10)

temp_label = tk.Label(root, text="氣溫：", font=("Microsoft JhengHei", 12))
temp_label.grid(row=2, column=0, sticky="w", padx=10)

rain_label = tk.Label(root, text="降雨機率：", font=("Microsoft JhengHei", 12))
rain_label.grid(row=3, column=0, sticky="w", padx=10)

time_label = tk.Label(root, text="資料時間：", font=("Microsoft JhengHei", 10))
time_label.grid(row=4, column=0, sticky="w", padx=10)

icon_label = tk.Label(root)
icon_label.grid(row=1, column=1, rowspan=4, padx=10)

forecast_frame = tk.Frame(root)
forecast_frame.grid(row=5, column=0, columnspan=2, pady=10)

system_time_label = tk.Label(root, text="", font=("Microsoft JhengHei", 10))
system_time_label.grid(row=6, column=0, columnspan=2, pady=10)

# 設定預設地區與縣市並載入天氣
region_var.set(list(region_map.keys())[0])  # 預設第一個地區（北部）
city_combo['values'] = region_map[region_var.get()]  # 根據預設地區設定城市
location_var.set(city_combo['values'][0])  # 預設第一個縣市（臺北市）
update_weather()  # 顯示天氣資訊

update_weather()
update_system_time()

root.mainloop()