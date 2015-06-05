# -----------------------------------------------------------------------------
# Filename: unit_test_regex_matching.py
# Author: Luis Alvarez
# This code performs a set of unit tests on
# the regex-matching.py module to make sure
# the code performs correctly.

# By creating a directory system with
# different sub-directories and files
# and matching a set of regular expressions
# to those files, one can compare
# the output of a recursive search
# for regular expression matches
# to the output of the creation
# search of the regular expressions.

# Import Statements -----------------------------------------------------------
import re
import random
import unittest
import shutil
import regex_matching as rm

class TestRegexMatches(unittest.TestCase):
    """ Class designed for unit testing. """
    
    def testEmptyRegex(self):
        """ Matching negative look-ahead 
        should always return null!. """
        top_dir, result = rm.create_directory_system(re.compile(''))
        key = re.compile('(?!)')
        self.assertEqual(sum(rm.search_for_regex_match(top_dir,key).values()),0)
        shutil.rmtree(top_dir)

    def testIntersection(self):
        """ Intersection of ^ should 
        not be equivalent. """
        top_dir, result = rm.create_directory_system(re.compile(''))
        key1 = re.compile('[abc]')
        key2 = re.compile('[^abc]')
        self.assertNotEqual(rm.search_for_regex_match(top_dir,key1),
                            rm.search_for_regex_match(top_dir,key2))
        shutil.rmtree(top_dir)
                            
    def testDirectorySystem(self):
        """ Perform a stochastic self-testign system,
        making sure recursive search is consistent
        with search performed on creation. """
    
        # Number of top directories to test 
        num_trials = 100
        # Generate possible regex list
        list_regex = [re.compile('['+rm.id_generator(size=random.randint(4,6))+']'+
                                 '['+rm.id_generator(size=random.randint(4,6))+']'+
                                 '['+rm.id_generator(size=random.randint(4,6))+']'+
                                 '[^'+rm.id_generator(size=random.randint(2,4))+']')
                                 for i in xrange(0,num_trials)]
        # Run through each directory, testing outputs
        for i in xrange(0,num_trials):
            key = random.choice(list_regex)
            top_dir, result = rm.create_directory_system(key)
            self.assertEqual(rm.search_for_regex_match(top_dir,key),result)
            # Remove created directory
            shutil.rmtree(top_dir)
        
        # <TODO> Add more tests!
        
if __name__ == '__main__':
    unittest.main()