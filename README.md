# StackbuilderWebcrawlerTest

Python web crawler using scraping techniques to extract the first 30 entries from <https://news.ycombinator.com/> and then filter them with tests

---

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Tests](#tests)

---

## Installation

### Prerequisites

- Python 3.x
- `pip` package manager

### Installation Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/ivanhitosm/StackbuilderWebcrawlerTest
   cd StackbuilderWebcrawlerTest

2. Install dependencies:

    ```bash
    pip install -r requirements.txt

### Usage

To run the Flask application:

    python app.py

### Available Filters

    Long Titles: Filters entries with more than five words in the title, ordered by the number of comments.
        Access via: http://localhost:5000/?filter=long_titles

    Short Titles: Filters entries with five or fewer words in the title, ordered by points.
        Access via: http://localhost:5000/?filter=short_titles

### Project Structure

    project-root/
    │
    ├── app.py               # Flask application setup and routes
    ├── crawler.py           # Functions for fetching and parsing HTML
    ├── filters.py           # Functions for filtering entries based on title length
    ├── templates/
    │   └── index.html       # HTML template for rendering entries
    ├── tests/
    │   ├── test_crawler.py  # Unit tests for crawler functions
    │   └── test_filters.py  # Unit tests for filters functions
    └── requirements.txt     # Dependencies for the project

### Tests

Explain how to run the tests and provide an overview of the testing framework used.
Running Tests

To run the tests using pytest:

    pytest

This will execute all the test files (test_crawler.py and test_filters.py) in the tests directory and display the test results.
