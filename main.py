from selenium import webdriver
import time
from datetime import datetime

# The browser we're using is Firefox
browser = webdriver.Firefox()

# Opens the page we indicated (in this case, a page that displays tweets tagged "Ecologie"
browser.get('https://walls.io/y683u')

# Collects multiple elements that have "checkin-message" as its class
tweets = browser.find_elements_by_class_name('checkin-message')

# Store the texts inside those elements in a variable
tweets_text = [tweet.text for tweet in tweets]

# Just waiting one second before changing page just in case, so that there are no problems
time.sleep(1)

# Change the current page to text analyser from Microsoft
browser.get('https://azure.microsoft.com/fr-fr/services/cognitive-services/text-analytics/')

# Search for the text area named "text-analytics-demo" in the page. This is where we will put the texts in the tweets
textArea = browser.find_element_by_id('text-analytics-demo')

# For as many tweets captured earlier
for tweet_text in tweets_text:
    # Delete what was in the text area
    textArea.clear()

    # Sometimes a popup asking to pay to use this service will appear.
    # Apparently just storing it in a variable gets rid of it. Yeah i don't know either ¯\_(ツ)_/¯
    popUp = browser.find_element_by_class_name('modal__close')

    # Puts the text of the current tweet in the text area
    textArea.send_keys(tweet_text)

    # Search for the button that's used to analyse the text
    analyseButton = browser.find_element_by_xpath("//input[@value='Analyser']")
    # And then it clicks on it
    analyseButton.click()

    # Waits 5 seconds for the page to reload.
    # It needs this otherwise the website won't have time to analyse the new text
    time.sleep(5)

    # Search for the part of the page where the result in json format is
    jsonResult = browser.find_element_by_class_name('json-result')
    # And then collects the innerHTML of the element
    jsonResultHTML = jsonResult.get_attribute('innerHTML')

    # I choose to name the json files this script produce by using the date and time to seconds
    now = datetime.now()
    formatedDateTime = now.strftime("%d-%m-%Y-%H-%M-%S")
    # Writes said file
    jsonFile = open(formatedDateTime+".json", "w")
    jsonFile.write(jsonResultHTML)
    # And then we're off to the next tweet, except if it's the last. If it's the last, then...

# We close the browser
browser.close()
