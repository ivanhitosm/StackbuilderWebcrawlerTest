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
from crawler import fetch_url, parse_entries, extract_entry, extract_title, extract_number, extract_points, extract_comments
from bs4 import BeautifulSoup
import requests

def test_fetch_url(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = 'Fake HTML content'
    mocker.patch('requests.get', return_value=mock_response)
    
    assert fetch_url('https://example.com') == 'Fake HTML content'

def test_parse_entries():
    html = """
    <tr class="athing" id="12345">
        <td align="right" class="title"><span class="rank">1.</span></td>
        <td valign="top" class="votelinks"><center><a id="up_12345" href="vote?id=12345&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td>
        <td class="title"><span class="titleline"><a href="https://example.com">Example title</a></span></td>
    </tr>
    <tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_12345">10 points</span> by <a href="user?id=test">test</a> <span class="age"><a href="item?id=12345">1 hour ago</a></span> | <a href="hide?id=12345&amp;goto=news">hide</a> | <a href="item?id=12345">5 comments</a>
    </td></tr>
    """
    entries = parse_entries(html)
    assert len(entries) == 1
    entry = entries[0]
    assert entry['title'] == 'Example title'
    assert entry['number'] == '1.'
    assert entry['points'] == 10
    assert entry['comments'] == 5

def test_extract_entry():
    row_html = """
    <tr class="athing" id="12345">
        <td align="right" class="title"><span class="rank">1.</span></td>
        <td valign="top" class="votelinks"><center><a id="up_12345" href="vote?id=12345&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td>
        <td class="title"><span class="titleline"><a href="https://example.com">Example title</a></span></td>
    </tr>
    """
    subtext_html = """
    <tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_12345">10 points</span> by <a href="user?id=test">test</a> <span class="age"><a href="item?id=12345">1 hour ago</a></span> | <a href="hide?id=12345&amp;goto=news">hide</a> | <a href="item?id=12345">5 comments</a>
    </td></tr>
    """
    row = BeautifulSoup(row_html, 'html.parser')
    subtext_row = BeautifulSoup(subtext_html, 'html.parser')
    row.find_next_sibling = lambda tag='tr': subtext_row  # Ensure the lambda accepts an argument
    
    entry = extract_entry(row)
    assert entry['title'] == 'Example title'
    assert entry['number'] == '1.'
    assert entry['points'] == 10
    assert entry['comments'] == 5

def test_extract_title():
    row_html = """
    <tr class="athing" id="12345">
        <td align="right" class="title"><span class="rank">1.</span></td>
        <td valign="top" class="votelinks"><center><a id="up_12345" href="vote?id=12345&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td>
        <td class="title"><span class="titleline"><a href="https://example.com">Example title</a></span></td>
    </tr>
    """
    row = BeautifulSoup(row_html, 'html.parser')
    assert extract_title(row) == 'Example title'

def test_extract_number():
    row_html = """
    <tr class="athing" id="12345">
        <td align="right" class="title"><span class="rank">1.</span></td>
    </tr>
    """
    row = BeautifulSoup(row_html, 'html.parser')
    assert extract_number(row) == '1.'

def test_extract_points():
    subtext_html = """
    <tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_12345">10 points</span>
    </td></tr>
    """
    subtext_row = BeautifulSoup(subtext_html, 'html.parser')
    assert extract_points(subtext_row) == 10

def test_extract_comments():
    subtext_html = """
    <tr><td colspan="2"></td><td class="subtext">
        <a href="item?id=12345">5 comments</a>
    </td></tr>
    """
    subtext_row = BeautifulSoup(subtext_html, 'html.parser')
    assert extract_comments(subtext_row) == 5

if __name__ == '__main__':
    pytest.main()
