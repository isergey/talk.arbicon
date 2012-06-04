# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import HttpResponseForbidden


from ..models import Poll, PollsMember, Choice, Vote
from forms import get_choices_form

@login_required
def index(request):

    if not PollsMember.is_member(request.user) and not request.user.is_superuser and not request.user.has_perm('arbicon_polls.view_journal'):
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
    is_member = PollsMember.is_member(request.user)
    if not is_member and not request.user.is_superuser and not request.user.has_perm('arbicon_polls.view_journal'):
        return HttpResponse(u"У Вас нет доступа к голосованиям.")

    poll = get_object_or_404(Poll, id=id)
    ChoicesForm = get_choices_form(poll)
    user_is_voted = poll.user_is_voted(request.user)

    form = None

    if request.method == 'POST':
        if not is_member:
            return HttpResponse(u"Вы не можете голосовать так как не являетесь участником голосований.")
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

    choices = list(Choice.objects.filter(poll=poll).order_by('id'))
    for choice in choices:
        votes = list(Vote.objects.select_related('poll_member').filter(choice=choice))
        choice.votes = 0
        for vote in votes:
            choice.votes += vote.poll_member.type.votes_count

    if choices:
        summ_votes = 0
        for choice in choices:
            summ_votes += choice.votes
        for choice in choices:
            if summ_votes == 0:
                choice.percent = u'0'
            else:
                choice.percent = u'%.2f' % (choice.votes * 100.0 / summ_votes)


    for choice in choices:
        print choice.percent

    return render(request, 'arbicon_polls/frontend/show.html', {
        'poll': poll,
        'form': form,
        'user_is_voted': user_is_voted,
        'choices': choices,
        'is_member': is_member
    })

@login_required
def journal(request, id):
    if not request.user.has_perm('arbicon_polls.view_journal'):
        return HttpResponseForbidden()
    poll = get_object_or_404(Poll, id=id)
    votes = Vote.objects.select_related().filter(poll=poll).order_by('-vote_date')
    return render(request, 'arbicon_polls/frontend/journal.html', {
        'poll': poll,
        'votes': votes,
    })


@login_required
def not_voted(request):
    votes = Vote.objects.all()
    voted_members_id = []
    for vote in votes:
        voted_members_id.append(vote.poll_member_id)
    voted_members_id = list(set(voted_members_id))
    not_voted_members = PollsMember.objects.select_related().all().exclude(id__in=voted_members_id)
    return render(request, 'arbicon_polls/frontend/not_voted.html', {
        'not_voted_members': not_voted_members,
    })
