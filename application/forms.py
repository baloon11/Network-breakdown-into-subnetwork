# coding: utf-8
from django import forms

class InputForm(forms.Form):

    first_bite=forms.ChoiceField(choices=[[i,i] for i in xrange(256)], label='')
    second_bite=forms.ChoiceField(choices=[[i,i] for i in xrange(256)], label='')
    third_bite=forms.ChoiceField(choices=[[i,i] for i in xrange(256)], label='')
    fourth_bite=forms.ChoiceField(choices=[[i,i] for i in xrange(256)], label='')

    mask=forms.ChoiceField(choices=[[i,i] for i in xrange(16,25)], label='')

    net_27=forms.IntegerField(label='')
    prs_or_unit_27=forms.ChoiceField(choices=[('%','%'),('unit','unit')], label='')

    net_28=forms.IntegerField(label='')
    prs_or_unit_28=forms.ChoiceField(choices=[('%','%'),('unit','unit')], label='')

    net_29=forms.IntegerField(label='')
    prs_or_unit_29=forms.ChoiceField(choices=[('%','%'),('unit','unit')], label='')

    net_30=forms.IntegerField(label='')
    prs_or_unit_30=forms.ChoiceField(choices=[('%','%'),('unit','unit')], label='')

