from base64 import b32encode
from io import BytesIO
from typing import TYPE_CHECKING, List

from lor_deckcodes.utils import write_varint
from lor_deckcodes.constants import CURRENT_FORMAT_VERSION, faction_mapping

if TYPE_CHECKING:
    from lor_deckcodes import CardCodeAndCount


def _get_set_faction_combinations(cards: List["CardCodeAndCount"]):
    set_faction_combinations = []
    sets = sorted(set([card.set for card in cards]))
    for card_set in sets:
        factions = sorted(set([card.faction for card in cards if card.set == card_set]))
        [set_faction_combinations.append((card_set, faction)) for faction in factions]
    set_faction_combinations = sorted(
        set_faction_combinations,
        key=lambda y: (
            len([card for card in cards if card.faction == y[1] and card.set == y[0]]), y[0], y[1],
        )
    )
    return set_faction_combinations


def _encode_card_block(data_stream: BytesIO, cards: List["CardCodeAndCount"]) -> None:
    set_faction_combinations = _get_set_faction_combinations(cards)
    write_varint(data_stream, len(set_faction_combinations))
    for card_set, faction in set_faction_combinations:
        faction_cards = [card for card in cards if card.faction == faction and card_set == card.set]
        write_varint(data_stream, len(faction_cards))
        write_varint(data_stream, card_set)
        write_varint(data_stream, faction_mapping.get(faction))
        for faction_card in faction_cards:
            write_varint(data_stream, faction_card.card_id)


def _encode_event_card_block(data_stream: BytesIO, cards: List["CardCodeAndCount"]) -> None:
    sorted_cards = sorted(cards, key=lambda y: y.card_code)
    for card in sorted_cards:
        write_varint(data_stream, card.count)
        write_varint(data_stream, card.set)
        write_varint(data_stream, faction_mapping.get(card.faction))
        write_varint(data_stream, card.card_id)


def encode_deck(cards: List["CardCodeAndCount"]) -> str:
    data = BytesIO()
    write_varint(data, CURRENT_FORMAT_VERSION)

    # 3 card copies
    three_copies = list(filter(lambda x: x.count == 3, cards))
    _encode_card_block(data, three_copies)
    # 2 card copies
    two_copies = list(filter(lambda x: x.count == 2, cards))
    _encode_card_block(data, two_copies)
    # 1 card copies
    one_copies = list(filter(lambda x: x.count == 1, cards))
    _encode_card_block(data, one_copies)

    # the remainder of the deck code is comprised of entries for cards with counts >= 4
    # this will only happen in Limited and special game modes.
    # the encoding is simply [count] [cardcode]
    more_copies = list(filter(lambda x: x.count > 3, cards))
    _encode_event_card_block(data, more_copies)

    data.seek(0)
    return b32encode(data.read()).decode().replace('=', '')
