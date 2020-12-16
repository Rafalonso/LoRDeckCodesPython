from unittest import TestCase
from lor_deckcodes.models import LoRDeck
import os


class BaseTestDeckcode(TestCase):
    def setUp(self):
        with open(f'{os.path.dirname(os.path.abspath(__file__))}/test_data.txt', 'rb') as f:
            deck_blocks = f.read().decode().split('\n\n')

        self.decks = {}
        for deck_block in deck_blocks:
            deckcode = deck_block.split('\n')[0]
            card_list = deck_block.split('\n')[1:]
            self.decks[deckcode] = LoRDeck(card_list)


class TestDeckcodeDecode(BaseTestDeckcode):
    def test_data_decode(self):
        for deckcode, card_list in self.decks.items():
            self.assertListEqual(list(LoRDeck.from_deckcode(deckcode)), list(card_list))


class TestDeckcodeEncode(BaseTestDeckcode):
    def test_data_decode(self):
        for card_list in self.decks.values():
            encoded_string = card_list.encode()
            decoded_string = LoRDeck.from_deckcode(encoded_string)
            self.assertListEqual(sorted(list(decoded_string)), sorted(list(card_list)))


class TestMixedSetFaction(TestCase):
    def test_issue_3(self):
        lor_cards = ['3:01NX020', '3:01NX012', '3:01NX040', '3:01NX015', '3:01NX030', '3:01PZ054',
                     '3:01NX037', '3:02NX004', '3:01PZ017', '1:01NX047', '3:01PZ052', '3:02NX003',
                     '3:01PZ039', '3:01NX002']
        deck = LoRDeck(lor_cards)
        deckstring = deck.encode()
        deck = LoRDeck.from_deckcode(deckstring)

        self.assertListEqual(sorted(lor_cards), sorted(list(deck)))


class TestOrderSetFaction(TestCase):
    def test_order(self):
        lor_cards = ['3:01SI015', '3:01SI044', '3:01SI048', '3:01SI054', '3:01FR003', '3:01FR012',
                     '3:01FR020', '3:02FR024', '3:01FR033', '3:01FR036', '3:01FR039', '3:01FR052',
                     '2:01FR004', '2:01SI005']
        deck = LoRDeck(lor_cards)
        deckstring = deck.encode()
        deck = LoRDeck.from_deckcode(deckstring)
        ordered_list = ['3:02FR024', '3:01SI015', '3:01SI044', '3:01SI048', '3:01SI054',
                        '3:01FR003', '3:01FR012', '3:01FR020', '3:01FR033', '3:01FR036',
                        '3:01FR039', '3:01FR052', '2:01FR004', '2:01SI005']
        self.assertListEqual(list(deck), ordered_list)


class TestMoreThan3Cards(TestCase):
    def test_more_than_3_order(self):
        lor_cards = ['3:01SI015', '3:01SI044', '3:01SI048', '3:01SI054', '3:01FR003', '3:01FR012',
                     '3:01FR020', '3:02FR024', '3:01FR033', '3:01FR036', '3:01FR039', '3:01FR052',
                     '2:01FR004', '4:01SI005']
        deck = LoRDeck(lor_cards)
        deckstring = deck.encode()
        deck = LoRDeck.from_deckcode(deckstring)
        ordered_list = ['3:02FR024', '3:01SI015', '3:01SI044', '3:01SI048', '3:01SI054',
                        '3:01FR003', '3:01FR012', '3:01FR020', '3:01FR033', '3:01FR036',
                        '3:01FR039', '3:01FR052', '2:01FR004', '4:01SI005']
        self.assertListEqual(list(deck), ordered_list)
