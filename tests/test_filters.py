import pytest
import sys
import os

# Get the current directory of the script
current_dir = os.path.dirname(__file__)

# Get the parent directory (project root)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Add the parent directory to the start of the system path.
# This allows the test files to import modules from the parent directory.
sys.path.insert(0, parent_dir)

from filters import filter_long_titles, filter_short_titles, word_count
def test_word_count():
    assert word_count("This is a test title") == 5
    assert word_count("Another title, with punctuation!") == 4
    assert word_count("") == 0
    assert word_count("Title") == 1
    assert word_count("A very very long title with many words indeed") == 9

def test_filter_long_titles():
    entries = [
        {'title': 'This is a short title', 'comments': 10, 'points': 50},
        {'title': 'This is a considerably longer title that should be filtered', 'comments': 30, 'points': 100},
        {'title': 'Another long title that has more words', 'comments': 20, 'points': 70}
    ]
    filtered = filter_long_titles(entries)
    assert len(filtered) == 2
    assert filtered[0]['comments'] == 30  # Entry with the most comments should come first
    assert filtered[1]['comments'] == 20  # Followed by the one with fewer comments

def test_filter_short_titles():
    entries = [
        {'title': 'Short', 'comments': 10, 'points': 50},
        {'title': 'Another short', 'comments': 30, 'points': 100},
        {'title': 'Tiny', 'comments': 20, 'points': 70}
    ]
    filtered = filter_short_titles(entries)
    assert len(filtered) == 3
    assert filtered[0]['points'] == 100  # Entry with the most points should come first
    assert filtered[1]['points'] == 70   # Followed by the one with fewer points
    assert filtered[2]['points'] == 50   # And so on

if __name__ == '__main__':
    pytest.main()