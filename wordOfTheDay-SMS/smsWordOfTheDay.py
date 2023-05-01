import os
from dotenv import load_dotenv
import json
import requests
import random
from twilio.rest import Client
load_dotenv()

# Load the English words dictionary from file
with open("../words_dictionary.json", "r") as f:
    english_words = json.load(f)

# Twilio API
account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)


# Set up the API endpoint and key

while True:
    # Select a random word from the dictionary
    word = random.choice(list(english_words.keys()))

    # Make the API request
    url = url_template = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={os.getenv('MERRIAM_WEB_API_KEY_COLG')}"
    response = requests.get(url)

    try:
        # Convert the response to JSON format
        json_data = json.loads(response.text)

        # Check if the word has a definition
        if len(json_data) > 0:
            # Get the first definition
            definition = json_data[0].get("shortdef", ["No definition found"])[0]
            wordOfTheDay = f"\nThe word of the day is {word}. \nThe defintion of {word} is: {definition}"
            break  # Exit the loop since we found a word with a definition
    except AttributeError:
        # Catch the AttributeError and keep trying with a different word
        pass
    except json.JSONDecodeError:
        # Catch the JSONDecodeError and keep trying with a different word
        pass
    except:
        # Catch any other exceptions and keep trying with a different word
        pass


message = client.messages \
				.create(
                     body=wordOfTheDay,
                     from_=os.getenv("TWILIO_FROM"),
                     to=os.getenv("TWILIO_TO")
                 )