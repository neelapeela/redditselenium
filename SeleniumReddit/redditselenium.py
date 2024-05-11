from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Get the search query from the request
    search_query = request.form.get('search_query')

    chrome_options = Options()
    chrome_options.add_argument('--headless=new')  # Run headlessly
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    image_preferences = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", image_preferences)

    # Initialize the WebDriver with Chrome options
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Open Google
    driver.get("https://www.google.com")
    driver.implicitly_wait(10)

    # Find the search box and enter the query
    search_box = driver.find_element(By.XPATH, "/html//textarea[@id='APjFqb']")
    search_box.send_keys(search_query + " review reddit")
    search_box.send_keys(Keys.RETURN)

    # Click on the first search result
    search_result = driver.find_element(By.XPATH, "//*[@jsname='UWckNb']")
    url = str(search_result.get_attribute("href"))
    url = url.split("/")
    redditurl = "/".join(url[:8])
    response = requests.get(redditurl+".json")

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data
        json_data = response.json()
        # Extract all comments from the parsed JSON data
        comments = [child['data']['body'] for child in json_data[1]['data']['children'] if child['kind'] == 't1']

    # Perform sentiment analysis and calculate average sentiment score
    datadict = {}
    sentimentscore = 0
    count = 0
    analyzer = SentimentIntensityAnalyzer()

    for comment in comments:
        text = comment
        datadict[text] = analyzer.polarity_scores(text)['compound']
        sentimentscore += analyzer.polarity_scores(text)['compound']
        count += 1

    sentimentscore = 50 + ((sentimentscore * 100) / (2 * count))

    # Close the WebDriver
    driver.quit()

    # Return the sentiment analysis results
    return render_template('results.html', sentiment_scores=datadict, average_sentiment_score=sentimentscore, originalurl=redditurl)

if __name__ == '__main__':
    app.run(debug=True)
