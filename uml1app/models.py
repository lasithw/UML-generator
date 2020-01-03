from django.db import models


# Create your models here.
class ClassNames(models.Model):
    names = models.TextField(max_length=500)

    def __str__(self):
        return self.names


class ClassAttributes(models.Model):
    names = models.TextField(max_length=500)
    attributes = models.TextField(max_length=500)


class ClassMethods(models.Model):
    names = models.TextField(max_length=500)
    methods = models.TextField(max_length=500)


class ClassLoop(models.Model):
    names = models.TextField(max_length=500)
    anotherclass = models.TextField(max_length=500)


class ClassRelationships(models.Model):#Inhritance
    names = models.TextField(max_length=500)


class IdentifiedAggrigations(models.Model):#Inhritance
    names = models.TextField(max_length=500)


class CompositionRelationship(models.Model):
    names = models.TextField(max_length=500)
    nextclass = models.TextField(max_length=500)


class NotIdentifiedClasses(models.Model):
    names = models.TextField(max_length=500)


class Seq_Items(models.Model):
    sender = models.TextField(max_length=500)
    reciever = models.TextField(max_length=500)
    Message = models.TextField(max_length=500)
    loop = models.TextField(max_length=500)
    MessageType = models.TextField(max_length=500)
    conditions = models.TextField(max_length=500)
    conditionMsg = models.TextField(max_length=500)
    elsemsg = models.TextField(max_length=500)
    sender_else = models.TextField(max_length=500)
    reciver_else = models.TextField(max_length=500)
    conditionBit = models.TextField(max_length=500)
    If_loop = models.TextField(max_length=500)
    else_loop = models.TextField(max_length=500)
    SeqId = models.TextField(max_length=500)


