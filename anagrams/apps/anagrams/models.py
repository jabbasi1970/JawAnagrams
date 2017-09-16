from django.db import models

# Create your models here.
class WordAnagrams(models.Model):
    class Meta:
        verbose_name = "WordAnagram"
        verbose_name_plural = "WordAnagrams"
    word = models.CharField(max_length=40)
    tries = models.IntegerField(default=1)
    def __unicode__(self):
        return self.word

class Suggestions(models.Model):
    class Meta:
        verbose_name = "Suggestion"
        verbose_name_plural = "Suggestions" 
    word = models.CharField(max_length=40)
    def __unicode__(self):
        return self.word

