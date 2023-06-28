import requests
import random
import time

WORD_SIZE = 5

def get_response(): 
    url = "https://agilec.cs.uh.edu/words"
    
    return requests.get(url).text
    
def parse_response(response):
    cleaned_response = response.strip()
    
    if(check_if_valid_list(cleaned_response)):
        raise ValueError("Response does not have a list") 
     
    return cleaned_response[1:-1].replace(' ','').split(',') if cleaned_response[1:-1] != "" else []
  
def check_if_valid_list(response):
    return not (response.startswith('[') and response.endswith(']'))

def get_random_word_given_a_seed(words, seed):

    if not hasattr(get_random_word_given_a_seed, 'seed') or get_random_word_given_a_seed.seed != seed:
        get_random_word_given_a_seed.seed = seed
        random.seed(seed)
    
    return random.choice(words) 

def get_a_random_word():
    seed = time.time()
    
    word = get_random_word_given_a_seed(parse_response(get_response()), seed)
    
    if(len(word) != WORD_SIZE):
        raise ValueError("Word length is not 5")

    return word.upper()
