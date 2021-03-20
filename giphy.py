from dotenv import load_dotenv
import os

import giphy_client
from giphy_client.rest import ApiException

from discord.ext import commands
load_dotenv()
TOKEN = os.getenv('GIPHY_TOKEN')


api_instance = giphy_client.DefaultApi()
config = {
    'api_key': TOKEN,
    'limit': 1,
    'rating': 'g'
}

def search_gif(term):
    try:
        api_response = api_instance.gifs_search_get(config['api_key'], limit=config['limit'], rating=config['rating'],q=term)
        return api_response.data[0].url
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)