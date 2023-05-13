from google_images_search import GoogleImagesSearch
from constants import CUSSTOM_SEARCH_API_KEY, CX_ID


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
    download_image("mcdonalds big mac", "temp", "big mac")
