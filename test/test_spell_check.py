import unittest
from unittest.mock import Mock, patch
from src.spell_check import get_response, parse_response, is_spelling_correct
from parameterized import parameterized


class SpellCheckTests(unittest.TestCase):
  
  def test_get_response(self):
    self.assertIsInstance(get_response("FAVOR"), str)

  @parameterized.expand([
    ('true', True),
    ('false', False)
  ])
  def test_parse_response_to_bool(self, response, expected_result):  
    self.assertEqual(parse_response(response), expected_result)
 
  def test_is_spelling_correct(self):    
    get_response = Mock(return_value='true')
    parse_response = Mock(return_value=True)

    with patch("src.spell_check.get_response", get_response):
      with patch("src.spell_check.parse_response", parse_response):
        self.assertTrue(is_spelling_correct("FAVOR"))

    get_response.assert_called()
    parse_response.assert_called_with("true") 
    
  def test_is_spelling_correct_passes_on_exception_to_caller(self):
    get_response = Mock(side_effect=ValueError)
    
    with patch("src.spell_check.get_response", get_response):
      with self.assertRaises(ValueError):
        is_spelling_correct("FAVOR")
    
if __name__ == '__main__': 
  unittest.main()
