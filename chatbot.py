#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PA6, CS124, Stanford, Winter 2016
# v.1.0.2
# Original Python code by Ignacio Cases (@cases)
# Ported to Java by Raghav Gupta (@rgupta93) and Jennifer Lu (@jenylu)
######################################################################
import csv
import math
import sys
import os
import re
import pprint

import numpy as np

from movielens import ratings
from random import randint
from PorterStemmer import PorterStemmer

class Chatbot:
    """Simple class to implement the chatbot for PA 6."""

    #############################################################################
    # `moviebot` is the default chatbot. Change it to your chatbot's name       #
    #############################################################################
    def __init__(self, is_turbo=False):
      self.name = 'moviebot'
      self.is_turbo = is_turbo
      self.read_data()
      self.binarize()

    #############################################################################
    # 1. WARM UP REPL
    #############################################################################

    def greeting(self):
      """chatbot greeting message"""
      #############################################################################
      # TODO: Write a short greeting message                                      #
      #############################################################################

      greeting_message = 'Hi, my name is "Arnold: The Movie Chatinator." I have seen 9125 movies till date! My friends say I am really good at giving movie recommendations. Maybe I could help you?'

      #############################################################################
      #                             END OF YOUR CODE                              #
      #############################################################################

      return greeting_message

    def goodbye(self):
      """chatbot goodbye message"""
      #############################################################################
      # TODO: Write a short farewell message                                      #
      #############################################################################

      goodbye_message = 'I hope you enjoy watching the movie! Remember to grab some popcorn buddy! Have a nice day!'

      #############################################################################
      #                             END OF YOUR CODE                              #
      #############################################################################

      return goodbye_message



    #############################################################################
    # 2. Modules 2 and 3: extraction and transformation                         #
    #############################################################################

    def process(self, input):
      """Takes the input string from the REPL and call delegated functions
      that
        1) extract the relevant information and
        2) transform the information into a response to the user
      """
      #############################################################################
      # TODO: Implement the extraction and transformation in this method, possibly#
      # calling other functions. Although modular code is not graded, it is       #
      # highly recommended                                                        #
      #############################################################################
      movies_file = "movies.txt"
      if self.is_turbo == True:
        response = 'processed %s in creative mode!!' % input
      else:

        titles = [x[0] for x in self.titles]
        # print titles

        response = 'processed %s in starter mode' % input

        regex1 = '\"(.*?)\"'
        matches = re.findall(regex1,input)
        if len(matches) < 1:
          random_responses1 = []
          random_responses1.append('Sorry, I dont understand what you are trying to say. Tell me about a movie you have seen.')
          random_responses1.append('Sorry, I dont think that is a movie. Could you give me a new movie?')
          random_responses1.append('Sorry, I dont understand the movie name. Please give me another one')
          # random.choice(random_responses1)
          index = randint(0,2)
          response = random_responses1[index]

        elif len(matches) > 1:
          random_responses2 = []
          random_responses2.append('Please tell me about one movie at a time. Go ahead.')
          random_responses2.append('Slow down. Give me a movie one at a time.')
          random_responses2.append('Hold up, I can only understand one movie at a time.')
          index = randint(0,2)
          response = random_responses2[index]

        else: 
          exists = False

          match = matches[0]
          match1 = "The " + match
          match2 = "A " + match
          match3 = "An " + match
          if match or match1 or match2 or match3 in titles:
            exists = True 
          for title in titles:
            pattern = re.compile('^(?:The |An |A )?' + match + '(?: \([0-9][0-9][0-9][0-9]\))?$')
            if pattern.match(title):
              print "Hello"
              exists = True
              break

          if not exists:
            random_responses3 = []
            random_responses3.append('Sorry I havent seen that movie before. Could you give me another movie?')
            random_responses3.append('Oops, I havent seen that myself. Guess I have something to do this weekend. Could you tell me about another movie?')
            random_responses3.append('I havent heard of that movie before. Could you tell me about another movie?')
            index = randint(0,2)
            response = random_responses3[index]
            
          else:
            sentence = re.findall(r"[\w']+|[.,!?;]", input.replace(match, ""))
            sentiment = 0
            negation = False
            
            for i in xrange(0,len(sentence)):
              word = sentence[i]
              
              wordSentiment = 0
              if self.sentiment[word] == 'pos':
                wordSentiment = 1
              else:
                wordSentiment = -1
              
              if negation:
                if word in [".", ",", ";", "?", "!"]:
                  negation = False
                else:
                  wordSentiment = -1*wordSentiment
              if word in ["not", "neither", "nor","never"]:
                negation = True
              
              sentiment += wordSentiment
            print sentiment
                
      return response


    #############################################################################
    # 3. Movie Recommendation helper functions                                  #
    #############################################################################

    def read_data(self):
      """Reads the ratings matrix from file"""
      # This matrix has the following shape: num_movies x num_users
      # The values stored in each row i and column j is the rating for
      # movie i by user j
      self.titles, self.ratings = ratings()
      reader = csv.reader(open('sentiment.txt', 'rb'))
      self.sentiment = dict(reader)


    def binarize(self):
      """Modifies the ratings matrix to make all of the ratings binary"""
      binary_threshold = 2.5
      for movie in xrange(0, len(self.ratings)):
        for user in xrange(0, len(self.ratings[movie])):
          rating = self.ratings[movie][user]
          if rating > binary_threshold:
            self.ratings[movie][user] = 1
          elif rating > 0:
            self.ratings[movie][user] = -1
          else:
            self.ratings[movie][user] = 0

    def distance(self, u, v):
      """Calculates a given distance function between vectors u and v"""
      # TODO: Implement the distance function between vectors u and v]
      # Note: you can also think of this as computing a similarity measure
      return numpy.dot(u,v)/(len(u)*len(v))


    def recommend(self, u):
      """Generates a list of movies based on the input vector u using
      collaborative filtering"""
      # TODO: Implement a recommendation function that takes a user vector u
      # and outputs a list of movies recommended by the chatbot

      pass


    #############################################################################
    # 4. Debug info                                                             #
    #############################################################################

    def debug(self, input):
      """Returns debug information as a string for the input string from the REPL"""
      # Pass the debug information that you may think is important for your
      # evaluators
      debug_info = 'debug info'
      return debug_info


    #############################################################################
    # 5. Write a description for your chatbot here!                             #
    #############################################################################
    def intro(self):
      return """
      Your task is to implement the chatbot as detailed in the PA6 instructions.
      Remember: in the starter mode, movie names will come in quotation marks and
      expressions of sentiment will be simple!
      Write here the description for your own chatbot!
      """


    #############################################################################
    # Auxiliary methods for the chatbot.                                        #
    #                                                                           #
    # DO NOT CHANGE THE CODE BELOW!                                             #
    #                                                                           #
    #############################################################################

    def bot_name(self):
      return self.name


if __name__ == '__main__':
    Chatbot()
