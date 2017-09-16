from django.contrib import admin
from models import WordAnagrams,Suggestions

class WordAnagramsAdmin(admin.ModelAdmin):
    list_display = ('word', 'tries')
    ordering = ("-tries", )

admin.site.register(WordAnagrams, WordAnagramsAdmin)
admin.site.register(Suggestions)
