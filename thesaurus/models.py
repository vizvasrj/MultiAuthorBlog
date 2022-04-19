from django.db import models


class Thesaurus(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name


class RelationsScore(models.Model):
    word = models.ForeignKey(Thesaurus, on_delete=models.CASCADE, related_name='words', db_index=True)
    related_word = models.ForeignKey(Thesaurus, on_delete=models.CASCADE, related_name='wordsr', db_index=True)
    score = models.IntegerField(db_index=True)
    syn = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.word} {self.related_word} {self.score}'
    
    class Meta:
        ordering = ('created',)