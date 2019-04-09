from channels.layers import get_channel_layer

from django.test import TestCase

from apps.chat.models import Room
from apps.chat.forms import RoomForm, RoomCodeForm
from apps.user.models import User


class ChatModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user', ip='100.10.1.0')
        self.room = Room.objects.create(name='test_name1', created_by=self.user)

    def test_create_room(self):
        room_data = {
            "name": "test_name2",
            "created_by": self.user.id
        }
        form = RoomForm(room_data)
        valid = form.is_valid()
        self.assertTrue(valid)
        self.room = form.save()

    def test_create_private_room(self):
        room_data = {
            "name": "test_name3",
            "created_by": self.user.id,
            "is_private": True
        }
        form = RoomForm(room_data)
        private_room = form.save()
        self.assertTrue(private_room.is_private)
        self.assertIsNotNone(private_room.roomcode_set.all().first())

    def test_create_roomcode(self):
        roomcode = {
            "room": self.room.id
        }
        form = RoomCodeForm(roomcode)
        valid = form.is_valid()
        self.assertTrue(valid)

class ChannelTestCase(TestCase):

    def setUp(self):
        self.channel_layer = get_channel_layer()

    def test_channel_layer(self):
        from asgiref.sync import async_to_sync
        message = {'type': 'hello'}
        async_to_sync(self.channel_layer.send)('test_channel', message)
        response = async_to_sync(self.channel_layer.receive)('test_channel')
        self.assertEqual(message, response)

