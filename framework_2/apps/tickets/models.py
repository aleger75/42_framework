from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


def validate_type(type):
    if type == '--------':
        raise ValidationError(u'Please enter a valid type')


class Tickets(models.Model):
    TYPE_DEFAULT = '--------'
    ADM = 'ADM'
    OTHER = 'Autre'
    BOX = 'Boite a idee'
    ACCOUNT = 'Compte'
    INTRA = 'Intra'
    LOGISTIC = 'Logistique'
    MOULINETTE = 'Moulinette'
    PEDAGO = 'Pedago'
    SUBJECTS = 'Sujets'
    TIG = 'TIG'
    VOGSPHERE = 'Vogsphere'
    TYPE_CHOICES = (
        (TYPE_DEFAULT, '--------'),
        (ADM, 'ADM'),
        (OTHER, 'Autre'),
        (BOX, 'Boite a idee'),
        (ACCOUNT, 'Compte'),
        (INTRA, 'Intra'),
        (LOGISTIC, 'Logistique'),
        (MOULINETTE, 'Moulinette'),
        (PEDAGO, 'Pedago'),
        (SUBJECTS, 'Sujets'),
        (TIG, 'TIG'),
        (VOGSPHERE, 'Vogsphere'),
    )
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    VERY_LOW = 5
    PRIORITY_CHOICES = (
        (CRITICAL, 'Critical'),
        (HIGH, 'High'),
        (NORMAL, 'Normal'),
        (LOW, 'Low'),
        (VERY_LOW, 'Very low'),
    )
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, default=TYPE_DEFAULT, validators=[validate_type],
                            help_text='Please choose the category closest to your issue.')
    title = models.CharField(max_length=100, verbose_name='Summary of the problem')
    body = models.TextField(verbose_name='Description of Issue')
    priority = models.IntegerField(max_length=1, choices=PRIORITY_CHOICES, default=NORMAL,
                                   help_text='Please select a priority carefully. If unsure, leave it as "Normal".')
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name='creator')
    staff = models.ForeignKey(User, related_name='staff', default=None, null=True, blank=False,
                              limit_choices_to={'is_staff': True})
    status = models.BooleanField(default=True, verbose_name='Opened')

    def __str__(self):
        return self.creator.username + ' - ' + self.title

    class Meta:
        verbose_name = 'Tickets'
        verbose_name_plural = 'Tickets'
        ordering = ['-status', 'priority', 'created']


class Answer(models.Model):
    answer = models.TextField()
    answer_date = models.DateTimeField(auto_now_add=True)
    answer_creator = models.ForeignKey(User, related_name='answer_creator')
    related = models.ForeignKey(Tickets)

    def __str__(self):
        return self.answer_creator.username + ' - ' + self.related.creator.username

    class Meta:
        ordering = ['answer_date']
