from django.test import TestCase
from models import WordAnagrams, Suggestions

class AnagramsTest(TestCase):

    def create_an_anagrams(self, word="test", tries=1):
        return WordAnagrams.objects.create(word=word, tries=tries)

    def test_anagrams_creation(self):
        w = self.create_an_anagrams()
        self.assertTrue(isinstance(w, WordAnagrams))
        self.assertEqual(w.__unicode__(), w.word)

class SuggestionsTest(TestCase):

    def create_suggestions(self, word="ppp"):
        return Suggestions.objects.create(word=word)

    def test_suggestions_creation(self):
        w = self.create_suggestions()
        self.assertTrue(isinstance(w, Suggestions))
        self.assertEqual(w.__unicode__(), w.word)
