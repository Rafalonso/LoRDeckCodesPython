from io import BytesIO
from typing import List
from itertools import product
from base64 import b32encode

from lor_deckcodes.utils import next_varint, decode_base32, write_varint
from lor_deckcodes.constants import faction_mapping


FORMAT_VERSION = 17


class CardCodeAndCount:
    @classmethod
    def from_card_string(cls, card_string: str):
        count, card_code = card_string.split(':')
        return cls(card_code, int(count))

    def __init__(self, card_code: str, count: int):
        self.card_code = card_code
        self.count = count

    def __str__(self):
        return f"{self.count}:{self.card_code}"

    @property
    def set(self) -> int:
        return int(self.card_code[:2])

    @property
    def faction(self) -> str:
        return self.card_code[2:4]

    @property
    def card_id(self) -> int:
        return int(self.card_code[4:])


class LoRDeckCodes:
    @classmethod
    def from_deckcode(cls, deckcode: str):
        return cls(decode_deck(deckcode))

    def __init__(self, cards=None):
        if cards:
            self.cards = [card if isinstance(card, CardCodeAndCount) else CardCodeAndCount.from_card_string(card)
                          for card in cards]
        else:
            self.cards = []

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        try:
            c = self.cards[self.n]
        except IndexError:
            raise StopIteration
        self.n += 1
        return str(c)

    def encode(self) -> str:
        return encode_deck(self.cards)


def _decode_card_block(n: int, data_stream: BytesIO) -> List[str]:
    card_block_list = []
    n_card_copies = next_varint(data_stream)
    for copies in range(n_card_copies):
        n_cards = next_varint(data_stream)
        set_number = next_varint(data_stream)
        faction = next_varint(data_stream)
        for card in range(n_cards):
            card_block_list.append(f'{n}:{set_number:02}{faction_mapping.get(faction)}{next_varint(data_stream):03}')
    return card_block_list


def _encode_card_block(data_stream: BytesIO, cards: List[CardCodeAndCount]) -> None:
    set_faction_combinations = list(product(
        set([card.set for card in cards]),
        set([card.faction for card in cards])))
    write_varint(data_stream, len(set_faction_combinations))

    set_faction_combinations = sorted(set_faction_combinations,
                                      key=lambda l: len([card for card in cards if card.faction == l[1]]))
    for card_set, faction in set_faction_combinations:
        faction_cards = [card for card in cards if card.faction == faction]
        write_varint(data_stream, len(faction_cards))
        write_varint(data_stream, card_set)
        write_varint(data_stream, faction_mapping.get(faction))
        for faction_card in faction_cards:
            write_varint(data_stream, faction_card.card_id)


def decode_deck(deckcode: str):
    all_cards = []
    decoded = decode_base32(deckcode)
    data = BytesIO(decoded)
    if next_varint(data) != 17:
        raise ValueError("Version/Format not supported.")

    # 3 card copies
    all_cards.extend(_decode_card_block(3, data))
    # 2 card copies
    all_cards.extend(_decode_card_block(2, data))
    # 1 card copies
    all_cards.extend(_decode_card_block(1, data))
    return all_cards


def card_encoder(card: str) -> int:
    """
    Card code should be the following: 3:01DE123
    """


def encode_deck(cards: List[CardCodeAndCount]) -> str:
    data = BytesIO()
    write_varint(data, FORMAT_VERSION)

    # 3 card copies
    three_copies = [card for card in cards if card.count == 3]
    _encode_card_block(data, three_copies)
    # 2 card copies
    two_copies = [card for card in cards if card.count == 2]
    _encode_card_block(data, two_copies)
    # 1 card copies
    one_copies = [card for card in cards if card.count == 1]
    _encode_card_block(data, one_copies)

    data.seek(0)
    return b32encode(data.read()).decode().replace('=', '')
