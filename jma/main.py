import requests
import flet as ft

# エンドポイントの定義
AREA_LIST_URL = "http://www.jma.go.jp/bosai/common/const/area.json"
FORECAST_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"


def main(page: ft.Page):
    page.title = "天気予報アプリ"
    page.scroll = "adaptive"

    # UIコンポーネント
    area_dropdown = ft.Dropdown(label="地域を選択", options=[], width=300)
    forecast_result = ft.Text(value="天気予報がここに表示されます。", size=16)
    fetch_button = ft.ElevatedButton(text="天気予報を取得", disabled=True)

    # 地域データ取得
    def fetch_area_list():
        try:
            response = requests.get(AREA_LIST_URL)
            response.raise_for_status()
            area_data = response.json()
            return {v["name"]: k for k, v in area_data["offices"].items()}
        except Exception as e:
            forecast_result.value = f"地域データの取得に失敗しました: {e}"
            page.update()
            return {}

    area_map = fetch_area_list()

    if area_map:
        area_dropdown.options = [ft.dropdown.Option(name) for name in area_map.keys()]
        fetch_button.disabled = False

    # 天気予報取得
    def fetch_forecast(e):
        selected_area = area_dropdown.value
        if selected_area and selected_area in area_map:
            area_code = area_map[selected_area]
            try:
                response = requests.get(FORECAST_URL.format(area_code=area_code))
                response.raise_for_status()
                forecast_data = response.json()

                # 予報データのパース
                forecasts = forecast_data[0]["timeSeries"][0]["areas"][0]["weathers"]
                forecast_result.value = f"{selected_area}の天気予報:\n" + "\n".join(forecasts)
            except Exception as e:
                forecast_result.value = f"天気予報の取得に失敗しました: {e}"
        else:
            forecast_result.value = "地域が選択されていません。"
        page.update()

    # ボタンイベント登録
    fetch_button.on_click = fetch_forecast

    # レイアウトに追加
    page.add(
        ft.Column(
            controls=[
                ft.Text("気象庁の天気予報アプリ", size=24, weight="bold"),
                area_dropdown,
                fetch_button,
                forecast_result,
            ],
            spacing=20,
        )
    )


# アプリケーションの実行
ft.app(target=main)
