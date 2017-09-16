from django.shortcuts import render
from models import WordAnagrams, Suggestions
import os


def build_dict(path):
    # Load in word file and sort each line.
    alpha = {}
    f = open(path, "r")
    for line in f.readlines():
        line = line.strip()
        key = sorted_line(line)

        # Add each line to a dictionary based on its sorted key.
        if key in alpha:
            v = alpha.get(key) + "," + line
            alpha[key] = v
        else:
            alpha[key] = line
    return alpha

def sorted_line(line):
    # Sort the chars in this line and return a string.
    chars = [c for c in line]
    chars.sort()
    return "".join(chars)

def anagram(alpha, line):
    # Return a list of anagrams from the dictionary.
    # ... Use a sorted string as the key.
    key = sorted_line(line)
    values = alpha.get(key, "NONE")
    return values.split(",")

def home(request):
    # Load our dictionary and use it.
    base=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dict=base+"/dictionary.txt"
    alpha = build_dict(dict)

    #word = raw_input("please input your word : ")
    word = 'NONE'
    results = 'NONE'
    if request.GET:
        word = request.GET['word']
        results = anagram(alpha, word)

	if "NONE" in results:
            new_word = Suggestions(word=word)
            new_word.save()
        elif word != "":
            existing_word, created = WordAnagrams.objects.get_or_create(word=word)
            if existing_word:
                existing_word.tries =  existing_word.tries + 1
                existing_word.save()

        print("Anagrams for %s" % word)
        print(results)
    ##################################
    return render(request, 'anagrams.html', {'anagrams': results, 'word': word, })
