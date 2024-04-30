# -*- coding: utf-8 -*-
"""finalevaluationstock.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/147tMiB3TwRJOX04uGV5uvUBC8uTPFeRE
"""

!pip install google.cloud.pubsub

pip install google-auth-oauthlib

from google.colab import auth
from google.auth.transport.requests import Request
from google.oauth2 import id_token

auth.authenticate_user()

import requests
from bs4 import BeautifulSoup
import time
from google.cloud import pubsub_v1

# Original code variables
ticker = "INFY"
url = f'https://www.google.com/finance/quote/{ticker}:NSE?hl=en'
class_name ="YMlKec fxKbKc"

def scrape_price(url, class_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Check if the element with the specified class name exists
    if soup.find(class_=class_name) is not None:
        price = float(soup.find(class_=class_name).text.strip()[1:].replace(",",""))
        return price
    else:
        return None

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
soup

project_id = "cts-0023"
topic_name = "test-123"

# Create a PublisherClient
publisher = pubsub_v1.PublisherClient()

# Create the topic path
topic_path = publisher.topic_path(project_id, topic_name)

# Main loop
for i in range(3):
    # Scrape price
    price = scrape_price(url, class_name)
    if price is not None:
        # Prepare message
        message =price

        # Publish message to Pub/Sub
        message_data_bytes = str(message).encode("utf-8")
        future = publisher.publish(topic_path, data=message_data_bytes)
        future.result()  # Wait for the message to be published
        print(price)
    else:
        print(f"Price for {ticker} not found")

    # Wait for 600 seconds
    time.sleep(100)

