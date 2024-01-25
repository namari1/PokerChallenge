import pytest
from poker_python_challenge_answers import Deck, Player, Card, hand_ranking, deal_cards, \
    winner_is, convert_card_to_numeric, is_flush, is_four_kind, is_three_kind, is_straight_flush, \
    is_straight, is_royal_flush, is_full_house, is_two_pair, is_pair, sort_cards


# Test Functions (boolean hand checks, hand ranking, dealing cards, sorting cards, converting
# cards to numeric values, and determining the winner)

@pytest.mark.parametrize("sample_hands, expected_result",
                         [(["2h", "As", "5c", "3d", "4h"], "Straight"),
                          (["2h", "Ah", "5h", "3h", "4h"], "Straight Flush"),
                          (["6h", "8h", "Qh", "3h", "10h"], "Flush"),
                          (["10s", "As", "Qs", "Js", "Ks"], "Royal Flush"),
                          (["10h", "10s", "10c", "10d", "4h"], "Four of a Kind"),
                          (["2h", "2s", "2c", "8d", "8h"], "Full House"),
                          (["5h", "5s", "5c", "3d", "4h"], "Three of a Kind"),
                          (["6h", "6s", "4c", "3d", "4h"], "Two Pair"),
                          (["Ah", "As", "5c", "3d", "4h"], "Pair"),
                          (["Kh", "As", "5c", "3d", "4h"], "High Card"), ])
def test_hand_ranking(sample_hands, expected_result):
    result = hand_ranking(sample_hands)
    assert result == expected_result


@pytest.mark.parametrize("players", [["Noor", "Hagen", "Sadie", "Kunai"]])
def test_deal_cards(players):
    result = deal_cards(players)
    for player, hand in result.items():
        assert player in players
        assert len(hand) == 5


@pytest.mark.parametrize("player_hands", [
    {'Noor': ['9h', '10s', '4h', 'Jc', '6c'], 'Hagen': ['6h', '6s', 'Qc', '9d', '9s'],
     'Sadie': ['10h', '2c', '5s', '2d', '3c'], 'Kunai': ['Ah', 'Qh', 'Kh', '10h', 'Jh']}])
def test_winner_is(player_hands):
    result = winner_is(player_hands)
    assert result == ["Kunai"]


@pytest.mark.parametrize("card", ["As"])
def test_convert_card_to_numeric(card):
    result = convert_card_to_numeric(card)
    assert result == (14, "s")


@pytest.mark.parametrize("hand, expected_result", [(["2h", "5h", "6h", "10h", "Ah"], True),
                                                   (["2h", "3s", "4c", "5d", "Ah"], False)])
def test_is_flush(hand, expected_result):
    sorted_hand = sort_cards(hand)
    result = is_flush(sorted_hand)
    assert result == expected_result


@pytest.mark.parametrize("hand, expected_result", [(["2h", "2s", "2c", "2d", "Ah"], True),
                                                   (["2h", "3s", "4c", "5d", "Ah"], False)])
def test_is_four_kind(hand, expected_result):
    sorted_hand = sort_cards(hand)
    result = is_four_kind(sorted_hand)
    assert result == expected_result


@pytest.mark.parametrize("hand, expected_result", [(["2h", "2s", "2c", "5d", "Ah"], True),
                                                   (["2h", "3s", "4c", "5d", "Ah"], False)])
def test_is_three_kind(hand, expected_result):
    sorted_hand = sort_cards(hand)
    result = is_three_kind(sorted_hand)
    assert result == expected_result


@pytest.mark.parametrize("hand, expected_result", [(["2h", "Ah", "3h", "5h", "4h"], True),
                                                   (["2h", "3s", "4c", "5d", "Ah"], False)])
def test_is_straight_flush(hand, expected_result):
    sorted_hand = sort_cards(hand)
    result = is_straight_flush(sorted_hand)
    assert result == expected_result


@pytest.mark.parametrize("hand, expected_result", [(["Ah", "2s", "3d", "4c", "5h"], True),
                                                   (["2h", "3s", "4c", "5d", "7h"], False)])
def test_is_straight(hand, expected_result):
    sorted_hand = sort_cards(hand)
    result = is_straight(sorted_hand)
    assert result == expected_result


@pytest.mark.parametrize("hand, expected_result", [(["10h", "Jh", "Qh", "Kh", "Ah"], True),
                                                   (["2h", "3s", "4c", "5d", "7h"], False)])
def test_is_royal_flush(hand, expected_result):
    sorted_hand = sort_cards(hand)
    result = is_royal_flush(sorted_hand)
    assert result == expected_result


@pytest.mark.parametrize("hand, expected_result", [(["10h", "10d", "10c", "5h", "5s"], True),
                                                   (["2h", "3s", "4c", "5d", "7h"], False)])
def test_is_full_house(hand, expected_result):
    sorted_hand = sort_cards(hand)
    result = is_full_house(sorted_hand)
    assert result == expected_result


@pytest.mark.parametrize("hand, expected_result", [(["10h", "10d", "6c", "7h", "6s"], True),
                                                   (["2h", "3s", "4c", "5d", "7h"], False)])
def test_is_two_pair(hand, expected_result):
    sorted_hand = sort_cards(hand)
    result = is_two_pair(sorted_hand)
    assert result == expected_result


@pytest.mark.parametrize("hand, expected_result", [(["10h", "10d", "3c", "4h", "5s"], True),
                                                   (["2h", "3s", "4c", "5d", "7h"], False)])
def test_is_pair(hand, expected_result):
    sorted_hand = sort_cards(hand)
    result = is_pair(sorted_hand)
    assert result == expected_result


# Test Classes

# TEST CARD
def test_card_creation():
    card = Card("h", "10")
    assert card.suit == "h"
    assert card.val == "10"
    assert card.card == "10h"
    assert card.num_card == ()


def test_card_show():
    card = Card("d", "K")
    result = card.show()
    assert result == "Kd"


def test_convert_card():
    card1 = Card("s", "A")
    card2 = Card("c", "4")

    result1 = card1.convert_card()
    result2 = card2.convert_card()

    assert card1.num_card == (14, "s")
    assert result1 == (14, "s")
    assert card2.num_card == (4, "c")
    assert result2 == (4, "c")


# TEST DECK
def test_deck_creation():
    deck = Deck()
    assert deck.cards == []


def test_deck_show():
    deck = Deck()
    result = deck.show()
    assert result == deck.cards


def test_deck_build():
    deck = Deck()
    deck.build()
    assert len(deck.cards)
    assert deck.cards == ['2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', 'Jh', 'Qh', 'Kh',
                          'Ah', '2d', '3d',
                          '4d', '5d', '6d', '7d', '8d', '9d', '10d', 'Jd', 'Qd', 'Kd', 'Ad', '2c',
                          '3c', '4c', '5c',
                          '6c', '7c', '8c', '9c', '10c', 'Jc', 'Qc', 'Kc', 'Ac', '2s', '3s', '4s',
                          '5s', '6s', '7s',
                          '8s', '9s', '10s', 'Js', 'Qs', 'Ks', 'As']


def test_deck_shuffle():
    deck = Deck()
    deck.build()
    original_order = deck.cards.copy()

    deck.shuffle()

    assert deck.cards != original_order


def test_deck_deal():
    deck = Deck()
    deck.build()
    original_cards = deck.cards.copy()

    card_dealt = deck.deal()
    assert card_dealt == original_cards[-1]
    assert len(deck.cards) == len(original_cards) - 1


# TEST PLAYER
def test_create_player():
    player = Player("Noor")
    assert player.name == "Noor"
    assert player.player_cards == []


def test_player_say_hello():
    player = Player("Noor")
    assert player.say_hello() == "Hi, I'm Noor!"


def test_player_draw_with_enough_cards():
    player = Player("Noor")
    deck = Deck()
    deck.build()

    original_cards = deck.cards.copy()
    result = player.draw(deck, num=5)
    assert result is True
    assert len(player.player_cards) == 5
    assert len(deck.cards) == len(original_cards) - 5


def test_player_draw_with_not_enough_cards():
    player = Player("Noor")
    deck = Deck()
    deck.build()
    result = player.draw(deck, num=53)
    assert result is False
    assert player.player_cards == []
    assert len(deck.cards) == 52


def test_player_show_hand():
    player = Player("Noor")
    deck = Deck()
    deck.build()
    player.draw(deck, num=5)
    result = player.show_hand()
    assert result == player.player_cards
