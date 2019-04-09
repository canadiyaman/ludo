import random
import string

from django import forms

from apps.chat.models import Room, RoomCode


class RoomForm(forms.ModelForm):

    def save(self, commit=False):
        room = super(RoomForm, self).save(commit=True)
        if room.is_private:
            room.create_roomcode()
        return room

    class Meta:
        model = Room
        fields = ('name', 'is_private', 'created_by')


class RoomCodeForm(forms.ModelForm):
    code = forms.CharField(required=False)

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not code:
            code = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
        return code

    class Meta:
        model = RoomCode
        fields = ('room', 'code')
