
# i/o imports
from urllib.request import urlopen
from bs4 import BeautifulSoup

# for rate limit
import time

# for formatting
from formatting import get_info

# for json output
import json

# tqdm for time
from tqdm import tqdm

# from google autocomplete :/
# def generate_jsonl_for_openai(data):
#     """Generates a JSONL string for OpenAI fine-tuning from a list of dictionaries."""

#     jsonl_data = ""
#     for item in data:
#         jsonl_data += json.dumps({"prompt": item["prompt"], "completion": item["completion"]}) + "\n"
#     return jsonl_data

"""
runs yahoo answers links thru wayback machine
gets OLDEST response 4 formatting consistency
"""
from waybackpy import WaybackMachineCDXServerAPI
def links2wayback(links):
    
    # stores results
    waybacked_links = []

    # iterates thru
    for link in tqdm(links):

        # rate limit
        time.sleep(5)

        # try/catch for robustness
        try:
            # idk what user_agent is..
            user_agent = ''
            cdx_api = WaybackMachineCDXServerAPI(link, user_agent)
            oldest = cdx_api.oldest()
            waybacked_links.append(oldest.archive_url)

        except:
            print(link)
            pass
    
    return waybacked_links


"""
main scraping method
INPUT: list of links
OUTPUT: jsonl of formatted data
for use in finetuning
"""
def links2jsonl(links):

    # list of dicts
    dict_list = []

    # iterates thru
    for link in tqdm(links):

        # rate limit
        time.sleep(5)

        # try/catch for robustness
        try:
            # url -> soup
            page = urlopen(link)
            html_bytes = page.read()
            # html = html_bytes.decode("utf-8")
            soup = BeautifulSoup(html_bytes, "html.parser")

            # gets info from url
            info = get_info(soup)

            # generates dict from info
            dict = {
                'prompt': '',
                'completion': info
            }
            dict_list.append(dict)

        except:
            print(link)
            pass

    return dict_list

# saves jsonl as file
TARGET_PATH = f"./data/jsonl"
def save_jsonl(data_list, name, target_path = TARGET_PATH):
    with open(f"{target_path}/{name}.jsonl", 'w') as f:
        for item in data_list:
            json.dump(item, f)
            f.write('\n')