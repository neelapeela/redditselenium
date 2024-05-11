# redditselenium
Basic Selenium proof of concept that takes a given query and scrapes the web for the most relevant reddit post and performs lexicon based sentiment analysis on each commenter's opinion. The program then spits out a final percentage score that represents the overall thread's sentiment towards the given query.

# dependencies
Note: Dependencies can be found in requirements.txt
- vaderSentiment - utilized the pre-trained lexicon based sentiment analysis model with 80% accurate results
- Selenium - Web scraped google and reddit to obtain comments in json format
- Flask - The most lightweight method of hosting the program on the web

# example uses
You can use this program when you need to see what people think about a certain 
- movie
- product
- game
- book
- travel destination

# example queries
- "La La Land"
- "Royal Enfield bikes"
- "India for vacation"
