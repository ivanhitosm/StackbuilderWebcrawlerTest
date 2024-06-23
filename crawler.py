import requests
from bs4 import BeautifulSoup
import logging

def fetch_url(url):
    """
    Fetches the content of the URL.
    
    :param url: URL to fetch
    :return: response text if the request is successful, otherwise None
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return None