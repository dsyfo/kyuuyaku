from django.db import models

class Char(models.Model):
    code = models.IntegerField(unique=True)
    value = models.CharField(max_length=1, null=True)
    printable = models.BooleanField(default=True)
    comment = models.TextField(null=True)


class CharBlock(models.Model):
    image_id = models.IntegerField(unique=True)


class CharBlockChar(models.Model):
    block = models.ForeignKey(CharBlock)
    char = models.ForeignKey(Char)
    location = models.IntegerField()

    class Meta:
        unique_together = [("block", "location")]


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
    ip = models.IntegerField(null=False)
    submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class CharVote(Vote):
    char = models.ForeignKey(Char)
    value = models.CharField(max_length=1, null=True)


class MessageVote(Vote):
    message = models.ForeignKey(Message)
    translation = models.TextField()
