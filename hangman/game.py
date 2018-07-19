from .exceptions import *
import random
WORD_LIST = ['rmotr', 'python', 'awesome']

class GuessAttempt(object):
  def __init__(self, character, hit = False, miss = False):
    self.guess = character 
    self.hit = hit 
    self.miss = miss 
    if hit == True and miss == True: 
      raise InvalidGuessAttempt
     
  def is_hit(self):
    if self.hit == True and self.miss== False: 
      return True  
    else: 
      return False 
    
  def is_miss(self):
    if self.miss == True and self.hit== False: 
      return True
    else: 
      return False 

    
class GuessWord(object):
  def __init__(self, word):
    if word == '': 
      raise InvalidWordException
    self.answer= word
    length = len(word)
    self.masked = '*'* length
    
  def perform_attempt(self, character):
    current_masked = self.answer
    if len(character) != 1:
      raise InvalidGuessedLetterException
    for char in self.answer: 
      # cater for case insentive case 
      # only mask those unrevealed answer
      if char.lower() != character.lower() and char.lower() not in self.masked:
        current_masked = current_masked.replace(char, '*')
    self.masked = current_masked.lower()
    if character.lower() in self.answer.lower(): 
      return GuessAttempt(character, hit = True)
    else: 
      return GuessAttempt(character, miss= True)


class HangmanGame(object):
  def __init__(self, a_list_of_words = None, number_of_guesses =5):
    HangmanGame.WORD_LIST = WORD_LIST
    if a_list_of_words is None: 
      a_list_of_words = HangmanGame.WORD_LIST
    self.remaining_misses = number_of_guesses 
    self.selection = self.select_random_word(a_list_of_words)
    self.word = GuessWord(self.selection)
    self.previous_guesses = [] 
    
  def guess(self, character): 
    # condition to raise exception when game won / finished 
    if '*' not in self.word.masked or self.remaining_misses == 0:
      self.finish = 1 
      raise GameFinishedException
    # return results of checking attempts
    ob = self.word.perform_attempt(character)
    self.previous_guesses.append(character.lower())
    # if attempt is wrong, reduce the remaining_misses
    if ob.is_miss():
      self.remaining_misses = self.remaining_misses -1 
    # raise condition after checking 
    if '*' not in self.word.masked:
      self.finish = 1
      self.won = True
      raise GameWonException
    # show results 
    if self.remaining_misses == 0:
      if '*' not in self.word.masked:
        self.finish = 1
        self.won = True 
        raise GameWonException
      else: 
        self.finish = 1
        self.won = False
        raise GameLostException
    return ob
  
  @classmethod
  def select_random_word(self,a_list_of_words):
    if a_list_of_words == []: 
      raise InvalidListOfWordsException
    word = random.choice(a_list_of_words)
    return word
  # for verification purposes 
  def is_finished(self):
    if self.finish == 1:
      return True 
    else: 
      return False 
  
  def is_won(self):
    if self.won == True: 
      return True
    else: 
      return False 
  
  def is_lost(self):
    if self.won == False: 
      return True
    else: 
      return False 
    
