#!/usr/bin/env python3

""" poem_generator.py:

Generates a poem from the corpora of two or more poets, using markov models.
Poet info is loaded from a json file created by poet_scraper.py
Poet corpus is loaded from a txt file created by corpus_scraper.py

author: ingversed
"""

from corpus_scraper import get_poets_json
import markovify, os, random

class Poem():
    DIR_PATH = 'PoemHunterTop500' # destination directory for text files
    poets_json = get_poets_json()
    
    def __init__(self, name_input=None, num_input=None):
        self.poet_num = num_input
        self.poet_names = name_input
        self._filenames, self._corpora, self._filesizes = [], [], []

        poets_json = type(self).poets_json

        if self.poet_num:
            # TODO: check for duplicates between random poet/s and input poet/s
            random_names = random.sample(poets_json.keys(), self.poet_num)
            self.poet_names.extend(random_names)

        if len(self.poet_names) < 2:
            raise RuntimeError('A minimum of two poets is required.')

        self._filenames = [poets_json[name]['link'][1:-1] for name in self.poet_names]
        
        # TODO: check if json model exists and use instead    
        for filename in self._filenames:
            poet_file = os.path.join(type(self).DIR_PATH, filename+'.txt')
            
            try:
                with open(poet_file, encoding='utf-8') as input_file:
                    corpus = input_file.read()
                    self._filesizes.append(os.path.getsize(poet_file))
                    self._corpora.append(corpus)
            except IOError:
                print("-- Error: " + filename + ".txt can't be found.")
    
    @property
    def poet_names(self):
        return self._names
    
    @poet_names.setter
    def poet_names(self, name_input):        
        if name_input:
            name_input = [name.strip() for name in name_input.split(',')]
            invalid_names = set(name_input).difference(type(self).poets_json.keys())
            if invalid_names:
                print('-- Excluding ' + ', '.join(invalid_names) + ' as not found in poets_json.')
            self._names = list(set(name_input).difference(invalid_names))
        else:
            self._names = []

    @property
    def poet_num(self):
        return self._poet_num
    
    @poet_num.setter
    def poet_num(self, num_input):
        try:
            num_input = num_input.strip()
            if num_input:
                self._poet_num = int(num_input)
                print(num_input)
            else:
                self._poet_num = None
        except ValueError:
                print("-- Ignoring number of poets as it's not a positive integer.")
                self._poet_num = None                

    def _get_weights(self):
        weights = []
        max_filesize = max(self._filesizes)
        
        for size in self._filesizes:
            weights.append(round(max_filesize/size, 2))

        return weights

    # TODO: check for json model
    def generate_poem(self):
        corpora_models = [markovify.NewlineText(corpus) for corpus in self._corpora] 
        corpora_combo = markovify.combine(corpora_models, self._get_weights())

        poem_lines = []

        while len(poem_lines) < 5:
            line = corpora_combo.make_sentence()
            if line != None:
                poem_lines.append(line)
                
        poem = '{}\n\n{}\n{}\n\n{}\n{}\n\n{}\n-- {}'.format(*poem_lines, poem_lines[0],
                                                            ' vs '.join(self.poet_names))
        print(poem)


name_message = 'Enter poet names (separated by commas), if required:'
name_input = input(name_message)    

num_message = 'Enter number of poets (as a positive int) to randomly select, if required:'
num_input = input(num_message)    

p = Poem(name_input, num_input)
p.generate_poem()



    
    
