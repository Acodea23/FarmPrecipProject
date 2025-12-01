import pandas as pd
import numpy as np
import requests


def write_txt(txt_name, r):
    with open(txt_name, "wb") as f:
        f.write(r.content)


def txt_to_csv(txt_name, colspecs, cols, csv_name):
    df = pd.read_fwf(txt_name, colspecs=colspecs, names=cols)
    df = df.apply(pd.to_numeric, errors='coerce')
    df.to_csv(csv_name, index=False)


def read_url_txt(url):
    # if url[-4] != ".txt":
    #     print("url must be a txt")
    r = requests.get(url)
    if r.status_code != 200:
        print(f"url status code is {r.status_code} not 200. Please check your url")
        return
    write_txt(r)
    txt_to_csv()