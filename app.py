from flask import Flask, render_template, request
from crawler import fetch_entries
from filters import filter_long_titles, filter_short_titles

app = Flask(__name__)

@app.route('/')
def index():
    entries = fetch_entries()
    filter_type = request.args.get('filter')
    if filter_type == 'long_titles':
        filtered_entries = filter_long_titles(entries)
    elif filter_type == 'short_titles':
        filtered_entries = filter_short_titles(entries)
    else:
        filtered_entries = entries
    return render_template('index.html', entries=filtered_entries)

if __name__ == '__main__':
    app.run(debug=True)
