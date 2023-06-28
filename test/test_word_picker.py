import unittest
from src.word_picker import get_response, parse_response, get_random_word_given_a_seed, get_a_random_word
from parameterized import parameterized
from unittest.mock import Mock, patch, ANY
import random

class WordPickerTests(unittest.TestCase):
    
    def test_get_response(self):
        self.assertIsInstance(get_response(), str)
    
    @parameterized.expand([
        ("[FAVOR, SKILL, PAINT]", ["FAVOR", "SKILL", "PAINT"]),
        ("[]", []),
    ])
    def test_parse_response_to_list(self, response, expected_result):
        self.assertEqual(parse_response(response), expected_result)

    def test_parse_response_raise_exception_for_no_list(self):
        with self.assertRaises(ValueError):
            parse_response("FAVOR") 
            
    def test_get_random_words_given_a_seed(self):
        word_list = ["FAVOR", "SKILL"]
        
        self.assertIn(get_random_word_given_a_seed(word_list, 55), word_list)
    
    def test_get_random_words_two_times_given_a_seed(self):
        word_list = ["FAVOR", "SKILL", "PAINT"]

        self.assertNotEqual(get_random_word_given_a_seed(word_list, 1), get_random_word_given_a_seed(word_list, 1))
      
    @patch("src.word_picker.get_random_word_given_a_seed", return_value="FAVOR")  
    @patch("src.word_picker.parse_response", return_value=["FAVOR", "SKILL", "PAINT"])
    @patch("src.word_picker.get_response", return_value='[FAVOR, SKILL, PAINT]')
    def test_get_a_random_word(self, get_response, parse_response, get_random_word_given_a_seed):        
        self.assertEqual(get_a_random_word(), "FAVOR")

        get_response.assert_called()
        parse_response.assert_called_with('[FAVOR, SKILL, PAINT]') 
        get_random_word_given_a_seed.assert_called_with(["FAVOR", "SKILL", "PAINT"], ANY)
        
    @patch("src.word_picker.get_random_word_given_a_seed", return_value="FAVOR")
    def test_get_a_random_word_calls_random_word_with_a_seed(self, get_random_word_given_a_seed):
        get_a_random_word()
        
        self.assertIsInstance(get_random_word_given_a_seed.call_args[0][1], float)
    
    @patch("src.word_picker.get_random_word_given_a_seed", return_value="FAVOR")
    def test_get_a_random_word_calls_random_word_with_different_seed_each_call(self, get_random_word_given_a_seed):
        get_a_random_word()
        get_a_random_word()
        
        self.assertNotEqual(get_random_word_given_a_seed.call_args_list[0][0][1], get_random_word_given_a_seed.call_args_list[1][0][1])
    
    def test_get_a_random_word_raise_exception_on_invalid_word_length(self):
        with patch("src.word_picker.get_random_word_given_a_seed", return_value="FOR"):
            with self.assertRaises(ValueError):
                get_a_random_word()

    def test_get_a_random_word_is_uppercase(self):
        with patch("src.word_picker.get_random_word_given_a_seed", return_value="print"):
            self.assertEqual(get_a_random_word(), "PRINT")