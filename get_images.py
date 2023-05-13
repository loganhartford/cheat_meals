from google_images_search import GoogleImagesSearch
from constants import CUSSTOM_SEARCH_API_KEY, CX_ID

import pandas as pd


def download_image(query, save_path, img_name):
    gis = GoogleImagesSearch(CUSSTOM_SEARCH_API_KEY, CX_ID)

    _search_params = {
        "q": query,
        "num": 1,
        "fileType": "jpg|png",
    }
    gis.search(search_params=_search_params, custom_image_name=img_name)
    img = gis.results()[0]
    img.download(save_path)
    return img.path


if __name__ == "__main__":
    # download all logos from data set
    df = pd.read_csv("fastfood.csv")
    names = df["restaurant"].unique()
    print(names)
    for name in names:
        print(download_image(name + " logo png", "logos", name.lower()))
