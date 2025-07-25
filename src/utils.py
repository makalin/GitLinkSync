import csv
import json
import logging
import os
from typing import List

def deduplicate_links(links: List[str]) -> List[str]:
    return list(set(links))

def export_links_to_csv(links, filename='links_export.csv'):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['url'])
        for link in links:
            writer.writerow([link])

def import_links_from_csv(filename='links_export.csv'):
    links = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            links.append(row['url'])
    return links

def export_links_to_json(links, filename='links_export.json'):
    with open(filename, 'w') as f:
        json.dump(links, f)

def import_links_from_json(filename='links_export.json'):
    with open(filename) as f:
        return json.load(f)

def setup_logging(logfile='gitlinksync.log'):
    logging.basicConfig(
        filename=logfile,
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s'
    )

def get_env_var(key, default=None):
    return os.environ.get(key, default) 