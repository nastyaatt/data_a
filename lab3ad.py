from spyre import server
import pandas as pd
import matplotlib.pyplot as plt

class StockExample(server.App):
    title = "NOAA data dropdown"

    inputs = [
        {
            "type": "dropdown",
            "label": "Оберіть тип індексу для графіку",
            "options": [
                {"label": "VCI", "value": "VCI"},
                {"label": "TCI", "value": "TCI"},
                {"label": "VHI", "value": "VHI"}
            ],
            "key": "data_type",
            "action_id": "update_data"
        },
        {
            "type": "dropdown",
            "label": "Оберіть область України:",
            "options": [
                {"label": "Вінницька", "value": "1"},
                {"label": "Волинська", "value": "2"},
                {"label": "Дніпропетровська", "value": "3"},
                {"label": "Донецька", "value": "4"},
                {"label": "Житомирська", "value": "5"},
                {"label": "Закарпатська", "value": "6"},
                {"label": "Запорізька", "value": "7"},
                {"label": "Івано-Франківська", "value": "8"},
                {"label": "Київська", "value": "9"},
                {"label": "Кіровоградська", "value": "10"},
                {"label": "Луганська", "value": "11"},
                {"label": "Львівська", "value": "12"},
                {"label": "Миколаївська", "value": "13"},
                {"label": "Одеська", "value": "14"},
                {"label": "Полтавська", "value": "15"},
                {"label": "Рівненська", "value": "16"},
                {"label": "Сумська", "value": "17"},
                {"label": "Тернопільська", "value": "18"},
                {"label": "Харківська", "value": "19"},
                {"label": "Херсонська", "value": "20"},
                {"label": "Хмельницька", "value": "21"},
                {"label": "Черкаська", "value": "22"},
                {"label": "Чернівецька", "value": "23"},
                {"label": "Чернігівська", "value": "24"},
                {"label": "Крим", "value": "25"}
            ],
            "key": "region",
            "action_id": "update_data"
        },
        {
            "type": "dropdown",
            "label": "Оберіть початковий тиждень:",
            "options": [{"label": str(i), "value": str(i)} for i in range(1, 53)],
            "key": "start_week",
            "action_id": "update_data"
        },
        {
            "type": "dropdown",
            "label": "Оберіть кінцевий тиждень:",
            "options": [{"label": str(i), "value": str(i)} for i in range(1, 53)],
            "key": "end_week",
            "action_id": "update_data"
        },
        {
            "type": 'slider',
            "label": 'Оберіть рік:',
            "min": 1981,
            "max": 2023,
            "key": 'year',
            "action_id": "update_data"
        },
    ]

    controls = [{"type": "hidden", "id": "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot"
        },
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        }
    ]

    def getData(self, params):
        region = int(params['region'])
        start_week = int(params['start_week'])
        end_week = int(params['end_week'])
        year = int(params['year'])

        # Завантаження тільки необхідних даних
        df = pd.read_csv('merged_df.csv', usecols=['year', 'week', 'ID', 'VCI', 'TCI', 'VHI'])
        df = df[(df['year'] == year) & (df['ID'] == region) & (df['week'] >= start_week) & (df['week'] <= end_week)]

        return df

    def getRegionName(self, region):
        region_mapping = {
            "1": "Вінничини",
            "2": "Волині",
            "3": "Дніпропетровщини",
            "4": "Донеччини",
            "5": "Житомирщини",
            "6": "Закарпаття",
            "7": "Запоріжжя",
            "8": "Івано-Франківщини",
            "9": "Київщини",
            "10": "Кіровоградщини",
            "11": "Луганщини",
            "12": "Львівщини",
            "13": "Миколаївщини",
            "14": "Одещини",
            "15": "Полтавщини",
            "16": "Рівненщини",
            "17": "Сумщини",
            "18": "Тернопільщини",
            "19": "Харківщини",
            "20": "Херсонщини",
            "21": "Хмельницька",
            "22": "Черкащини",
            "23": "Чернівців",
            "24": "Чернігівщини",
            "25": "Криму"
        }
        return region_mapping.get(str(region), "")

    def getPlot(self, params):
        df = self.getData(params)
        data_type = params['data_type']
        y_label = data_type
        year = params['year']
        region = params['region']
        region_name = self.getRegionName(region)
        start_week = params['start_week']
        end_week = params['end_week']

        plt_obj = df.plot(x='week', y=data_type, legend=False)
        plt_obj.set_ylabel(y_label)
        plt_obj.set_xlabel("Тижні")
        plt_obj.set_title(f"{data_type} графік для {region_name}, {year} рік, {start_week}-{end_week} тижні")
        fig = plt_obj.get_figure()
        return fig

    def getHTML(self, params):
        df = self.getData(params)
        return df.to_html()

    def getResult(self, params):
        return {
            "plot": self.getPlot(params),
            "table_id": self.getHTML(params)
        }

app = StockExample()
app.launch()

