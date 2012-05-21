# -*- coding: utf-8 -*-
import datetime
from django.conf import settings

from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from arbicon.models import Organisation

ACTIVE_CHOICES = (
    (0, u'Нет'),
    (1, u'Да'),
)

class Poll(models.Model):
    title = models.CharField(verbose_name=u'Тема голосования', max_length=255,unique=True)
    start_poll_date = models.DateTimeField(verbose_name=u'Дата начала голосования', db_index=True)
    end_poll_date = models.DateTimeField(verbose_name=u'Дата окончания голосования', db_index=True)
    active = models.IntegerField(verbose_name=u'Активно?', default=ACTIVE_CHOICES[0],choices=ACTIVE_CHOICES, db_index=True)
    create_date = models.DateTimeField(verbose_name=u'Дата создания',auto_now_add=True)
    show_results = models.BooleanField(verbose_name=u'Показывать результаты', default=False)
    show = models.BooleanField(verbose_name=u'Показывать голосование в списке голосований', default=False, db_index=True)
    order = models.IntegerField(default=100, verbose_name=u'Порядок вывода голосования в списке', db_index=True)
    class Meta:
        verbose_name = u"голосование"
        verbose_name_plural = u"голосования"

    def __unicode__(self):
        return self.title

    def clean(self):
        if self.start_poll_date >= self.end_poll_date:
            raise ValidationError(u'Дата окончания голосования должна быть больше даты начала')


    def is_active(self):
        if not self.active:
            return False
        now = datetime.datetime.now()
        if self.start_poll_date > now:
            return False

        if self.end_poll_date < now:
            return False
        return True

    @staticmethod
    def get_polls():
        return Poll.objects.filter(show=True)

    def make_vote(self, user, choice):
        poll_member = PollsMember.objects.get(user=user)
        vote = Vote(poll_member=poll_member, choice=choice, poll=self)
        vote.save()

    def get_choices(self):
        return list(Choice.objects.filter(poll=self))

    def user_is_voted(self, user):
        """
        Проголосовал ли пользовтаель
        """
        try:
            poll_member = PollsMember.objects.get(user=user)
        except PollsMember.DoesNotExist:
            return False

        if Vote.objects.filter(poll_member=poll_member, poll=self).count():
            return True
        else:
            return False

class Choice(models.Model):
    poll = models.ForeignKey(Poll, verbose_name=u'Голосование, к которому относится вопрос')
    title = models.CharField(max_length=255, verbose_name=u'название варианта ответа')
    votes = models.IntegerField(verbose_name=u'Количество голосов', default=0)
    class Meta:
        unique_together = (("poll", "title"),)
        verbose_name = u"вариант ответа"
        verbose_name_plural = u"варианты ответов"

    def __unicode__(self):
        return self.title

    def clean(self):

        if self.id:
            old = Choice.objects.get(id=self.id)
            if old.votes != self.votes:
                self.votes = old.votes
        else:
            self.votes = 0


class MemberType(models.Model):
    name = models.CharField(verbose_name=u'Назвние', max_length=64, unique=True)
    votes_count = models.IntegerField(default=1, verbose_name=u'Количество голосов (вес голоса)')
    class Meta:
        verbose_name = u"тип участника голосований"
        verbose_name_plural = u"типы участников голосований"

    def __unicode__(self):
        return self.name

    def clean(self):
        if self.votes_count < 1:
            raise ValidationError(u'Количество голосов должно быть положительным числом')


class PollsMember(models.Model):
    user = models.ForeignKey(User, unique=True, verbose_name=u'Пользователь')
    organisation = models.ForeignKey(Organisation, verbose_name=u'Организация',null=True, blank=True)
    type = models.ForeignKey(MemberType, verbose_name=u'Тип членства')
    class Meta:
        verbose_name = u"участник голосований"
        verbose_name_plural = u"участники голосований"

    def __unicode__(self):
        return u'%s: %s' % (self.user, self.organisation)

    @staticmethod
    def is_member(user):
        if PollsMember.objects.filter(user=user).count():
            return True
        else:
            return False

    @staticmethod
    def get_member(user):
        try:
            return  PollsMember.objects.get(user=user)
        except PollsMember.DoesNotExist:
            return None

    def clean(self):
        if PollsMember.objects.filter(organisation=self.organisation):
            raise ValidationError(u'К организации уже прикреплен пользователь')

class Vote(models.Model):
    poll_member = models.ForeignKey(PollsMember, verbose_name=u'Проголосовавший участник')
    poll = models.ForeignKey(Poll, verbose_name=u'Голосование')
    choice = models.ForeignKey(Choice, verbose_name=u'Вариант ответа')
    vote_date = models.DateTimeField(verbose_name=u'Дата голосования', db_index=True, auto_now_add=True)
    class Meta:
        unique_together = (("poll_member", "poll"),)
        ordering = ['-vote_date']
        verbose_name = u"голос"
        verbose_name_plural = u"журнал голосов"
        permissions = (
            ("view_journal", "Can see journal of poll's votes"),
            )

    def clean(self):
        if not self.choice.poll.active:
            raise ValidationError(u'Голосование не активно')
        now = datetime.datetime.now()
        if self.choice.poll.start_poll_date > now:
            raise ValidationError(u'Голосование еще не запущено')

        if self.choice.poll.end_poll_date < now:
            raise ValidationError(u'Время для голосования закончилось')


from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver


@receiver(pre_save, sender=Vote)
def vote_pre_save(instance, **kwargs):
    votes_count = instance.poll_member.type.votes_count
    # если происходит добавление нового объектае, то пересчитываем голоса
    if not instance.id:
        choice = instance.choice
        choice.votes = choice.votes + votes_count
        choice.save()


@receiver(pre_delete, sender=Vote)
def vote_pre_delete(instance, **kwargs):
    votes_count = instance.poll_member.type.votes_count
    choice = Choice.objects.get(id=instance.choice_id)
    if choice.votes:
        choice.votes -= votes_count
        choice.save()