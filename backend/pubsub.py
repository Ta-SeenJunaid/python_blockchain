import time

from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-b4cd8a40-95e9-11eb-9adf-f2e9c1644994'
pnconfig.publish_key = 'pub-c-e3b28220-ed06-47e2-9273-1e6ef65b2d1b'
pubnub = PubNub(pnconfig)

TEST_CHANNEL = 'TEST_CHANNEL'


class Listener(SubscribeCallback):
    def message(self, pubnub, message_object):
        print(f'\n-- Channel: {message_object.channel} | Message: {message_object.message}')


pubnub.add_listener(Listener())

class PubSub():
    def __init__(self):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels([TEST_CHANNEL]).execute()
        self.pubnub.add_listener(Listener())

    def publish(self, channel, meessage):
        """
        Publish the message object to the channel
        """
        self.pubnub.publish().channel(channel).message(meessage).sync()


def main():
    pubsub = PubSub()

    time.sleep(3)

    pubsub.publish(TEST_CHANNEL, { 'foo': 'bar' })


if __name__ == '__main__':
    main()