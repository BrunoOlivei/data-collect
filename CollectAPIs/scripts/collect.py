import json
import time
import logging
from datetime import datetime
from typing import Optional

import requests
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Collector:
    def __init__(self, url: str, service_name: str, instance_name: str) -> None:
        self.url = url
        self.service_name = service_name
        self.instance_name = instance_name

    def get_content(self, **kwargs) -> Optional[requests.Response]:
        try:
            resp = requests.get(self.url, params=kwargs)
            return resp
        except Exception as e:
            raise e

    def save_as_json(self, data: dict, save_timestamp: int) -> None:
        try:
            with open(f"./data/{self.service_name}/{self.instance_name}/json/{save_timestamp}.json", 'w') as f:
                json.dump(data, f)
            logging.info(f"Data saved in json format - {self.url}")
        except Exception as e:
            raise e

    def save_as_parquet(self, data: dict, save_timestamp: int) -> None:
        try:
            df = pd.DataFrame(data)
            df.to_parquet(
                f'./data/{self.service_name}/{self.instance_name}/parquet/{save_timestamp}.parquet',
                index=False
            )
            logging.info(f"Data saved in parquet format - {self.url}")
        except Exception as e:
            raise e

    def save_data(self, data: dict, file_format: str = "json") -> None:
        save_timestamp = round(datetime.now().timestamp() * 1000)

        if file_format == 'json':
            self.save_as_json(data, save_timestamp)

        elif file_format == 'dataframe':
            self.save_as_parquet(data, save_timestamp)

    def get_and_save(self, save_format: str = 'json',  **kwargs) -> Optional[dict]:
        resp = self.get_content(**kwargs)
        if resp.status_code == 200:
            data = resp.json()
            self.save_data(data, save_format)
            return data
        else:
            logging.error(f"Error for {self.url}: {resp.status_code} - {resp.reason}")

    def get_last_date(self, data: dict) -> Optional[datetime.date]:
        last_date = None
        if self.service_name == "TabNews" and "updated_at" in data[-1]:
            last_date = datetime.strptime(data[-1]['updated_at'], "%Y-%m-%dT%H:%M:%S.%fZ").date()
        if self.service_name == "JovemNerd" and 'published_at' in data[-1]:
            last_date = datetime.strptime(data[-1]['published_at'], "%Y-%m-%dT%H:%M:%S%z").date()
        return last_date

    def auto_exec(self, save_format: str, date_stop: datetime.date, **kwargs):
        page = kwargs.get('page', 1)
        while True:
            logging.info(f"Collecting page {page} from {self.url}")
            data = self.get_and_save(save_format=save_format, **kwargs)
            if data is None:
                logging.error(f"Error on collecting data from {self.url}, await 15 minutes")
                time.sleep(60 * 15)
            else:
                if len(data) == 0:
                    logging.info(f"No more data to collect from {self.url}")
                    break
                last_date = self.get_last_date(data)
                if last_date < date_stop:
                    logging.info(f"Last date collected: {last_date} from {self.url}")
                    break
                elif len(data) < 100:
                    logging.info(f"No more data to collect from {self.url}")
                    break
                page += 1
                kwargs['page'] = page
                time.sleep(5)


service_name = "JovemNerd"

if service_name == "JovemNerd":
    url = "https://api.jovemnerd.com.br/wp-json/jovemnerd/v1/nerdcasts/"
    params = {
        "page": 1,
        "per_page": 1000
    }
    instance_name = "episodes"
    date_stop = datetime(2000, 1, 1).date()
elif service_name == "TabNews":
    url = "https://www.tabnews.com.br/api/v1/contents"
    params = {
        "page": 1,
        "per_page": 100,
        "strategy": "new"
    }
    instance_name = "contents"
    date_stop = datetime(2024, 7, 1).date()

# Collect Jovem Nerd PodCasts Data
collect = Collector(url, service_name, instance_name)
collect.auto_exec(save_format='json', date_stop=date_stop, **params)
