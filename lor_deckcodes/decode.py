from io import BytesIO
from typing import List


from lor_deckcodes.utils import next_varint, decode_base32
from lor_deckcodes.constants import faction_mapping, CURRENT_FORMAT_VERSION, SUPPORTED_VERSIONS


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


def _decode_event_card_block(data_stream: BytesIO) -> List[str]:
    n_card_copies = next_varint(data_stream)
    set_number = next_varint(data_stream)
    faction = next_varint(data_stream)
    num = next_varint(data_stream)
    return [f'{n_card_copies}:{set_number:02}{faction_mapping.get(faction)}{num:03}']


def decode_deck(deckcode: str):
    all_cards = []
    decoded = decode_base32(deckcode)
    data = BytesIO(decoded)
    if next_varint(data) not in SUPPORTED_VERSIONS:
        raise ValueError("Version/Format not supported.")

    # 3 card copies
    all_cards.extend(_decode_card_block(3, data))

    # 2 card copies
    all_cards.extend(_decode_card_block(2, data))

    # 1 card copies
    all_cards.extend(_decode_card_block(1, data))

    # 4+ card copies (Events only)
    while True:
        try:
            all_cards.extend(_decode_event_card_block(data))
        except EOFError:
            break
    return all_cards


