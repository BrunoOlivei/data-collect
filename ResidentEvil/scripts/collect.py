import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import logging
import json
import pandas as pd


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

with open('resident_evil_headers.json', 'r') as f:
    headers = json.load(f)


def get_content(url: str):
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise Exception(f"Error: {resp.status_code} - {resp.reason}")
    return resp


def get_character_data(soup: BeautifulSoup):
    try:
        content = (soup.find("div", class_="td-page-content")
                   .find_all("p")[1]
                   .find_all("em"))
    except Exception as e:
        raise e

    dataset = {}
    if len(content) > 1:
        for i in content:
            try:
                key, value = i.text.split(":")
                key = key.strip(" ")
                dataset[key] = value.strip(" ")
            except Exception as e:
                logging.error(f"Error on unpacking data: {e}")
        return dataset
    else:
        for i in content:
            try:
                attributes = i.text.split("\n")
                for j in attributes:
                    key, value = j.split(":")
                    key = key.strip(" ")
                    dataset[key] = value.strip(" ")
            except Exception as e:
                logging.error(f"Error on unpacking data: {e}")
        return dataset


def get_apparences(soup: BeautifulSoup):
    try:
        appearances = (soup.find("div", class_="td-page-content")
                       .find("h4")
                       .find_next()
                       .find_all("li"))
    except Exception as e:
        raise e
    appearances_list = [i.text for i in appearances]
    return appearances_list


def get_characters_info(url: str):
    response = get_content(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    character = None
    try:
        character = get_character_data(soup)
    except Exception as e:
        logging.error(f"Error on get character data for {url}: {e}")
    else:
        try:
            character['appearances'] = get_apparences(soup)
        except Exception as e:
            logging.error(f"Error on get appearances data for {url}: {e}")
    return character


def get_characters_links():
    url = 'https://www.residentevildatabase.com/personagens'

    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')

    characters_links = [
        i['href'] for i in (soup.find("div", class_="td-page-content")
                            .find_all("a"))
    ]
    return characters_links


def get_all_characters_info():
    characters_links = get_characters_links()
    data = []
    for character_link in tqdm(characters_links):
        try:
            d = get_characters_info(character_link)
            if d:
                d['link'] = character_link
                name = character_link.strip("/").split("/")[-1].replace("-", " ").title()
                d['name'] = name
            else:
                logging.error(f"Error on get character info {character_link}")
            data.append(d)
        except Exception as err:
            logging.error(f"Error on get character info {character_link}: {err}")
    return data


def save_data(data):
    df = pd.DataFrame(data)
    df.to_parquet('data/raw.parquet', index=False)


if __name__ == '__main__':
    data = get_all_characters_info()
    save_data(data)
    logging.info("Data saved successfully")
