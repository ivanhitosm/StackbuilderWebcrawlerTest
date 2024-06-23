import re

def word_count(title):
    """
    Counts the number of words in a title, ignoring symbols and considering only spaced words.
    
    :param title: Title string
    :return: Number of words
    """
    words = re.findall(r'\b\w+\b', title)
    return len(words)

def filter_long_titles(entries):
    """
    Filters entries with more than five words in the title and orders them by the number of comments (descending).
    
    :param entries: List of dictionaries containing entry details
    :return: Filtered and sorted list of dictionaries
    """
    filtered = [entry for entry in entries if word_count(entry['title']) > 5]
    return sorted(filtered, key=lambda x: x['comments'], reverse=True)

def filter_short_titles(entries):
    """
    Filters entries with five or fewer words in the title and orders them by points (descending).
    
    :param entries: List of dictionaries containing entry details
    :return: Filtered and sorted list of dictionaries
    """
    filtered = [entry for entry in entries if word_count(entry['title']) <= 5]
    return sorted(filtered, key=lambda x: x['points'], reverse=True)
