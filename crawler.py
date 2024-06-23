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

def parse_entries(html):
    """
    Parses HTML content and extracts entries from Hacker News.
    
    :param html: HTML content to parse
    :return: List of dictionaries containing entry details
    """
    soup = BeautifulSoup(html, 'html.parser')
    entries = []

    # Find all entries with class="athing"
    rows = soup.find_all('tr', class_='athing')

    for row in rows:
        entry = extract_entry(row)
        if entry:
            entries.append(entry)

    return entries

def extract_entry(row):
    """
    Extracts relevant information (title, number, points, comments) from a single HTML row.
    
    :param row: BeautifulSoup Tag object representing a table row
    :return: Dictionary containing entry details
    """
    title = extract_title(row)
    number = extract_number(row)
    subtext_row = row.find_next_sibling('tr')
    points = extract_points(subtext_row)
    comments = extract_comments(subtext_row)
    
    return {
        'title': title,
        'number': number,
        'points': points,
        'comments': comments
    }

def extract_title(row):
    """
    Extracts the title from a row.
    
    :param row: BeautifulSoup Tag object representing a table row
    :return: Title string
    """
    title_span = row.find('span', class_='titleline')
    if title_span:
        title_a = title_span.find('a')
        return title_a.text.strip() if title_a else 'Title Not Found'
    return 'Title Not Found'

def extract_number(row):
    """
    Extracts the rank number from a row.
    
    :param row: BeautifulSoup Tag object representing a table row
    :return: Number string
    """
    rank_span = row.find('span', class_='rank')
    return rank_span.text.strip() if rank_span else 'Rank Not Found'

def extract_points(subtext_row):
    """
    Extracts the points from the subtext row.
    
    :param subtext_row: BeautifulSoup Tag object representing a subtext row
    :return: Points integer
    """
    points_elem = subtext_row.find('span', class_='score')
    return int(points_elem.text.split()[0]) if points_elem else 0

def extract_comments(subtext_row):
    """
    Extracts the number of comments from the subtext row.
    
    :param subtext_row: BeautifulSoup Tag object representing a subtext row
    :return: Comments integer
    """
    comments_elem = subtext_row.find('a', string=lambda s: 'comment' in s.lower())
    return int(comments_elem.text.split()[0]) if comments_elem and comments_elem.text.split()[0].isdigit() else 0

def fetch_entries(url="https://news.ycombinator.com/"):
    """
    Fetches and parses Hacker News entries.
    
    :param url: URL of the Hacker News page (default: "https://news.ycombinator.com/")
    :return: List of dictionaries containing entry details
    """
    html = fetch_url(url)
    if html:
        return parse_entries(html)
    return []
