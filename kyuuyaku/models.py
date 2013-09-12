from django.db import models
from collections import Counter
from random import choice

class Char(models.Model):
    code = models.IntegerField(unique=True)
    value = models.CharField(max_length=1, null=True)
    printable = models.BooleanField(default=True)
    comment = models.TextField(null=True)
    votes = models.IntegerField(default=0)

    approx_low = 999999

    @staticmethod
    def get_lowvote_char():
        chars = Char.objects.filter(votes__lte=Char.approx_low).all()
        if chars:
            return choice(chars)
        else:
            return choice(Char.objects.all())

    def save(self):
        if Char.approx_low >= self.votes:
            Char.approx_low = self.votes + 1
        super(Char, self).save()


class CharBlock(models.Model):
    image = models.TextField(unique=True, null=True)


class CharBlockChar(models.Model):
    block = models.ForeignKey(CharBlock)
    char = models.ForeignKey(Char)
    segment = models.IntegerField()
    location = models.IntegerField()

    class Meta:
        unique_together = [("block", "segment", "location")]


class CharBlockOCR(models.Model):
    block = models.ForeignKey(CharBlock)
    segment = models.IntegerField()
    text = models.TextField(null=True)

    class Meta:
        unique_together = [("block", "segment")]


class Message(models.Model):
    pointer = models.IntegerField(unique=True)
    data = models.TextField(null=False)
    text = models.TextField(null=True)


class Vote(models.Model):
    ip = models.CharField(max_length=15)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CharVote(Vote):
    char = models.ForeignKey(Char)
    value = models.CharField(max_length=1, null=True)

    class Meta:
        unique_together = [("ip", "char")]

    def save(self):
        super(CharVote, self).save()
        values = [cv.value for cv in self.char.charvote_set.all()]
        if values:
            c = Counter(values)
            if len(values) > 1:
                ((x,m), (y,n)) = tuple(c.most_common(2))
                if m == n:
                    self.char.value = None
                else:
                    self.char.value = x
            else:
                self.char.value, _ = c.most_common(1)[0]
        self.char.votes = len(values)
        self.char.save()


class MessageVote(Vote):
    message = models.ForeignKey(Message)
    translation = models.TextField()

    class Meta:
        unique_together = [("ip", "message")]
