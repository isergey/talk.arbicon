from django.contrib import admin
from models import Poll, PollsMember, Choice, Vote, MemberType
from django import forms
from django.contrib.auth.models import User

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2

class PollAdmin(admin.ModelAdmin):
    list_display = ('title','start_poll_date', 'end_poll_date', 'is_active', 'create_date', 'show_results', 'show')
    inlines = [ChoiceInline]
admin.site.register(Poll, PollAdmin)


#class ChoiceAdmin(admin.ModelAdmin):
#    list_display = ('poll','title', 'votes')
#admin.site.register(Choice, ChoiceAdmin)




class PollsMemberForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.order_by('username'))

    class Meta:
        model = PollsMember

class PollsMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'organisation', 'type')
    form = PollsMemberForm
admin.site.register(PollsMember, PollsMemberAdmin)


class VoteAdmin(admin.ModelAdmin):
    list_display = ('poll_member','poll', 'choice', 'vote_date')
admin.site.register(Vote, VoteAdmin)


class MemberTypeAdmin(admin.ModelAdmin):
    list_display = ('name','votes_count')
admin.site.register(MemberType, MemberTypeAdmin)