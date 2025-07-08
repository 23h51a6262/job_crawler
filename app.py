from flask import Flask, render_template, request, send_file
from scraper import scrape_internships
import webbrowser
from threading import Timer

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    internships = []
    keyword = ''
    if request.method == 'POST':
        keyword = request.form['keyword']
        internships = scrape_internships(keyword)
    return render_template('index.html', internships=internships, keyword=keyword)

@app.route('/download')
def download():
    return send_file('internships.csv', as_attachment=True)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True)
