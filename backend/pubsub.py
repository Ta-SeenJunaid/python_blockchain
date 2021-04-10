import time

from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from backend.blockchain.block import Block

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-b4cd8a40-95e9-11eb-9adf-f2e9c1644994'
pnconfig.publish_key = 'pub-c-e3b28220-ed06-47e2-9273-1e6ef65b2d1b'
pubnub = PubNub(pnconfig)


CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK'
}


class Listener(SubscribeCallback):
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def message(self, pubnub, message_object):
        print(f'\n-- Channel: {message_object.channel} | Message: {message_object.message}')

        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json_to_block(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)
            try:
                self.blockchain.replace_chain(potential_chain)
                print(f'\n Successfully replace the local chain')
            except Exception as e:
                print(f'\n Failed to replace chain: {e}')


# pubnub.add_listener(Listener(blockchain))


class PubSub():
    def __init__(self, blockchain):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain))

    def publish(self, channel, meessage):
        """
        Publish the message object to the channel
        """
        self.pubnub.publish().channel(channel).message(meessage).sync()

    def broadcast_block(self, block):
        self.publish(CHANNELS['BLOCK'], block.to_json())


def main():
    pubsub = PubSub()

    time.sleep(3)

    pubsub.publish(CHANNELS['TEST'], { 'foo': 'bar' })


if __name__ == '__main__':
    main()