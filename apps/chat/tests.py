from channels.layers import get_channel_layer

from django.test import TestCase


class ChannelTestCase(TestCase):

    def setUp(self):
        self.channel_layer = get_channel_layer()

    def test_channel_layer(self):
        from asgiref.sync import async_to_sync
        message = {'type': 'hello'}
        async_to_sync(self.channel_layer.send)('test_channel', message)
        response = async_to_sync(self.channel_layer.receive)('test_channel')
        self.assertEqual(message, response)

