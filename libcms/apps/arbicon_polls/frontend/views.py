# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse


from ..models import Poll, PollsMember, Choice, Vote
from forms import get_choices_form
@login_required
def index(request):

    if not PollsMember.is_member(request.user):
        return HttpResponse(u"У Вас нет доступа к голосованиям.")

    polls = Poll.get_polls()
    poll_member = PollsMember.get_member(request.user)
    member_votes = Vote.objects.filter(poll__in=polls, poll_member=poll_member)
    voted_polls = []
    for member_vote in member_votes:
        voted_polls.append(member_vote.poll_id)
    voted_polls = list(set(voted_polls))
    for poll in polls:
        if poll.id in voted_polls:
            poll.voted = True

    return render(request, 'arbicon_polls/frontend/index.html', {
        'polls': polls
    })

@login_required
def show(request, id):

    if not PollsMember.is_member(request.user):
        return HttpResponse(u"У Вас нет доступа к голосованиям.")

    poll = get_object_or_404(Poll, id=id)
    ChoicesForm = get_choices_form(poll)
    user_is_voted = poll.user_is_voted(request.user)

    form = None
    choices = []
    if request.method == 'POST':

        if user_is_voted:
            return HttpResponse(u'Вы уже отдали голос в этом голосовании')
        form = ChoicesForm(request.POST)

        if form.is_valid():
            choice =  form.cleaned_data['choice']
            poll.make_vote(user=request.user, choice=choice)
            return render(request,'arbicon_polls/frontend/thanks.html',{
                'poll': poll
            })
    else:
        if not user_is_voted:
            form = ChoicesForm()
        else:
            choices = list(Choice.objects.filter(poll=poll))

    if choices:
        summ_votes = 0
        for choice in choices:
            summ_votes += choice.votes
        for choice in choices:
            choice.percent = u'%.2f' % (choice.votes * 100.0 / summ_votes)


    for choice in choices:
        print choice.percent

    return render(request, 'arbicon_polls/frontend/show.html', {
        'poll': poll,
        'form': form,
        'user_is_voted': user_is_voted,
        'choices': choices
    })


