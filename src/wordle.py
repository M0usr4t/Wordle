from enum import Enum
from collections import Counter

class Match(Enum):
  EXACT = "EXACT" 
  EXISTS = "EXISTS"
  NO_MATCH = "NO_MATCH"

class Game(Enum):
  WIN = "WIN"
  LOSS = "LOSS"
  IN_PROGRESS = "IN_PROGRESS"
  WRONG_SPELLING = "WRONG_SPELLING"

WORD_SIZE = 5
MAX_ATTEMPTS = 6

def tally(target, guess):
  if(len(guess) != WORD_SIZE):
    raise ValueError("guess word length doesn't match with target word length") 
  
  return [tally_for_position(target, guess, position) for position in range(0, WORD_SIZE)]

def tally_for_position(target, guess, position):
  if(target[position]==guess[position]):
    return Match.EXACT

  current_letter = guess[position]
  
  exact_position_occurences = count_exact_position_match(target, guess, current_letter)
  non_exact_position_occurences = count_all_letter_match_at_position(WORD_SIZE, target, current_letter) - exact_position_occurences
  
  current_position_letter_occurences_in_guess_letter = count_all_letter_match_at_position(position+1, guess, current_letter)

  return Match.EXISTS if non_exact_position_occurences >= current_position_letter_occurences_in_guess_letter else Match.NO_MATCH 

def count_exact_position_match(target, guess, current_letter):
  all_exact_match = list(filter(lambda letter: letter[0] == letter[1], zip(target, guess)))
  all_exact_match = ''.join(list(map(lambda letter_tuple: letter_tuple[0], all_exact_match)))
  
  return Counter(all_exact_match)[current_letter]

def count_all_letter_match_at_position(length, word, current_letter):
  return Counter(word[0:length])[current_letter]

def get_game_info(position_status, target, attempts):
  game_won = check_win(position_status) 
  
  game_status = Game.LOSS if attempts + 1 >= MAX_ATTEMPTS and not game_won else Game.WIN if game_won else Game.IN_PROGRESS
  game_message = get_game_message(game_status, target, attempts + 1)
  
  return game_status, game_message


def check_win(position_status):
  return all(position_status[position] == Match.EXACT for position in range(0, WORD_SIZE))

def get_game_message(status, target, attempts):
  if(status == Game.WIN):
    return get_winning_message(attempts)
      
  return "" if status == Game.IN_PROGRESS else f"It was {target}, better luck next time"

def get_winning_message(attempts):
  winning_message = {1: "Amazing", 2: "Splendid", 3: "Awesome"}
  return winning_message.get(attempts, "Yay")

def play(target, guess, attempts, is_spelling_correct=lambda word: True):
  if(attempts >= MAX_ATTEMPTS):
    raise IndexError("Illegal attempts")
  
  if(is_spelling_correct(guess)):
    position_status = tally(target, guess) 
    
    game_status, game_message = get_game_info(position_status, target, attempts)
    
    return {"attempts": attempts + 1, "response": position_status, "game_status": game_status, "game_message": game_message}
  
  return {"attempts": attempts, "response": "", "game_status": Game.WRONG_SPELLING}
