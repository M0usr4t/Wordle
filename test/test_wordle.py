import unittest
from unittest.mock import Mock, patch
from src.wordle import Match, Game, tally, play
from parameterized import parameterized

EXACT = Match.EXACT
EXISTS = Match.EXISTS
NO_MATCH = Match.NO_MATCH

WIN = Game.WIN
LOSS = Game.LOSS
IN_PROGRESS = Game.IN_PROGRESS
WRONG_SPELLING = Game.WRONG_SPELLING

class WordleTests(unittest.TestCase):
  
  def test_canary(self):
    self.assertTrue(True)

  @parameterized.expand([
    ("FAVOR", "FAVOR", [EXACT, EXACT, EXACT, EXACT, EXACT]),
    ("FAVOR", "TESTS", [NO_MATCH, NO_MATCH, NO_MATCH, NO_MATCH, NO_MATCH]),
    ("FAVOR", "RAPID", [EXISTS, EXACT, NO_MATCH, NO_MATCH, NO_MATCH]),
    ("FAVOR", "MAYOR", [NO_MATCH, EXACT, NO_MATCH, EXACT, EXACT]),
    ("FAVOR", "RIVER", [NO_MATCH, NO_MATCH, EXACT, NO_MATCH, EXACT]),
    ("FAVOR", "AMAST", [EXISTS, NO_MATCH, NO_MATCH, NO_MATCH, NO_MATCH]),
    ("SKILL", "SKILL", [EXACT, EXACT, EXACT, EXACT, EXACT]),
    ("SKILL", "SWIRL", [EXACT, NO_MATCH, EXACT, NO_MATCH, EXACT]),
    ("SKILL", "CIVIL", [NO_MATCH, EXISTS, NO_MATCH, NO_MATCH, EXACT]),
    ("SKILL", "SHIMS", [EXACT, NO_MATCH, EXACT, NO_MATCH, NO_MATCH]),
    ("SKILL", "SILLY", [EXACT, EXISTS, EXISTS, EXACT, NO_MATCH]),
    ("SKILL", "SLICE", [EXACT, EXISTS, EXACT, NO_MATCH, NO_MATCH])
  ])

  def test_tally(self, target, guess, expected_result):
    self.assertEqual(tally(target, guess), expected_result) 
  
  @parameterized.expand([
    ("FAVOR", "FOR"),
    ("FAVOR", "FERVER") 
    ])
  def test_tally_raise_exception_for_invalid_guess_word_length(self, target, guess):
    with self.assertRaises(ValueError):
      tally(target, guess)   
      
  @parameterized.expand([
    ("FAVOR", "FAVOR", 0, {"attempts": 1, "response": [EXACT, EXACT, EXACT, EXACT, EXACT], "game_status": WIN, "game_message": "Amazing"}),
    ("FAVOR", "TESTS", 0, {"attempts": 1, "response": [NO_MATCH, NO_MATCH, NO_MATCH, NO_MATCH, NO_MATCH], "game_status": IN_PROGRESS, "game_message": ""}),
    ("FAVOR", "FAVOR", 1, {"attempts": 2, "response": [EXACT, EXACT, EXACT, EXACT, EXACT], "game_status": WIN, "game_message": "Splendid"}),
    ("FAVOR", "TESTS", 1, {"attempts": 2, "response": [NO_MATCH, NO_MATCH, NO_MATCH, NO_MATCH, NO_MATCH], "game_status": IN_PROGRESS, "game_message": ""}),
    ("FAVOR", "FAVOR", 2, {"attempts": 3, "response": [EXACT, EXACT, EXACT, EXACT, EXACT], "game_status": WIN, "game_message": "Awesome"}),
    ("FAVOR", "TESTS", 2, {"attempts": 3, "response": [NO_MATCH, NO_MATCH, NO_MATCH, NO_MATCH, NO_MATCH], "game_status": IN_PROGRESS, "game_message": ""}),
    ("FAVOR", "FAVOR", 3, {"attempts": 4, "response": [EXACT, EXACT, EXACT, EXACT, EXACT], "game_status": WIN, "game_message": "Yay"}),
    ("FAVOR", "TESTS", 3, {"attempts": 4, "response": [NO_MATCH, NO_MATCH, NO_MATCH, NO_MATCH, NO_MATCH], "game_status": IN_PROGRESS, "game_message": ""}),
    ("FAVOR", "FAVOR", 4, {"attempts": 5, "response": [EXACT, EXACT, EXACT, EXACT, EXACT], "game_status": WIN, "game_message": "Yay"}),
    ("FAVOR", "TESTS", 4, {"attempts": 5, "response": [NO_MATCH, NO_MATCH, NO_MATCH, NO_MATCH, NO_MATCH], "game_status": IN_PROGRESS, "game_message": ""}),
    ("FAVOR", "FAVOR", 5, {"attempts": 6, "response": [EXACT, EXACT, EXACT, EXACT, EXACT], "game_status": WIN, "game_message": "Yay"}),
    ("FAVOR", "TESTS", 5, {"attempts": 6, "response": [NO_MATCH, NO_MATCH, NO_MATCH, NO_MATCH, NO_MATCH], "game_status": LOSS, "game_message": "It was FAVOR, better luck next time"}),
  ])
  def test_attempt_guess(self, target, guess, attempts, expected_result):
    self.assertEqual(play(target, guess, attempts), expected_result)     
 
  @parameterized.expand([
  ("FAVOR", "FOR", 0)
  ])
  def test_play_raise_exception_for_invalid_guess_word_length(self, target, guess, attempts):
    with self.assertRaises(ValueError):
      play(target, guess, attempts)
      
  @parameterized.expand([
    ("FAVOR", "FAVOR", 6),
    ("FAVOR", "TESTS", 7)
  ])
  def test_play_raise_exception_for_illegal_attempts(self, target, guess, attempts):
    with self.assertRaises(IndexError):
      play(target, guess, attempts)

  @parameterized.expand([
    ("FAVOR", "FAVOR", 0, {"attempts": 1, "response": [EXACT, EXACT, EXACT, EXACT, EXACT], "game_status": WIN, "game_message": "Amazing"}),
    ("FAVOR", "RIVER", 0, {"attempts": 1, "response": [NO_MATCH, NO_MATCH, EXACT, NO_MATCH, EXACT], "game_status": IN_PROGRESS, "game_message": ""})
  ])
  def test_play_with_correct_spelling(self, target, guess, attempts, expected_result):    
      is_spelling_correct = Mock() 
      is_spelling_correct.return_value = True
      
      self.assertEqual(play(target, guess, attempts, is_spelling_correct), expected_result)
      is_spelling_correct.assert_called_with(guess)  
      
  @parameterized.expand([
    ("FAVOR", "FAVOR", 0, {"attempts": 0, "response": "", "game_status": WRONG_SPELLING}),
    ("FAVOR", "RIVER", 1, {"attempts": 1, "response": "", "game_status": WRONG_SPELLING}) 
  ])
  def test_play_with_incorrect_spelling(self, target, guess, attempts, expected_result):
    is_spelling_correct = Mock() 
    is_spelling_correct.return_value = False
    
    self.assertEqual(play(target, guess, attempts, is_spelling_correct), expected_result)
    is_spelling_correct.assert_called_with(guess)  
    
  def test_play_passes_on_exception_to_caller(self):
    is_spelling_correct = Mock(side_effect=ValueError)
    
    with self.assertRaises(ValueError):
      play("FAVOR", "FAVOR", 0, is_spelling_correct)

if __name__ == '__main__': 
  unittest.main()
