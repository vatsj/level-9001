
# i/o imports
from urllib.request import urlopen
from bs4 import BeautifulSoup

# for rate limit
import time

# for formatting
from unused.formatting import get_info

# for json output
import json

# from google autocomplete :/
# def generate_jsonl_for_openai(data):
#     """Generates a JSONL string for OpenAI fine-tuning from a list of dictionaries."""

#     jsonl_data = ""
#     for item in data:
#         jsonl_data += json.dumps({"prompt": item["prompt"], "completion": item["completion"]}) + "\n"
#     return jsonl_data

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
    for link in links:

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
            print("error on", link)
            pass

    return dict_list

# saves jsonl as file
TARGET_PATH = f"./data/jsonl"
def save_jsonl(data_list, name, target_path = TARGET_PATH):
    with open(f"{target_path}/{name}.jsonl", 'w') as f:
        for item in data_list:
            json.dump(item, f)
            f.write('\n')