""" Random mod providing random functions to shuffle a list and select random items from a list,
Counter mod to use for determining two pair hand"""
import random
from collections import Counter


# Part 1: Poker Hands
def convert_card_to_numeric(card):
    """ Function to convert card as string into card as a tuple with its rank as an int and its
    suit as a string"""

    # Getting the rank of the card by getting everything but the last element in the string which
    # is the suit
    rank_str = card[:-1]
    suit = card[-1]

    # Making a dictionary with the face cards and their numeric values
    face_card_values = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    # If the rank is a face card, getting the associated numeric value of it and saving it to a
    # new variable, rank_numeric
    if rank_str in face_card_values:
        rank_numeric = face_card_values[rank_str]
    # Otherwise, converting the string rank into a numeric value
    else:
        rank_numeric = int(rank_str)

    # Returning the card as a tuple of the integer rank and the string suit
    return rank_numeric, suit


# Create distinct functions that will determine if a player's sorted cards belong to one of the
# 10 different hands in poker
def is_full_house(sorted_hand):
    """ Function that returns true if sorted hand is a full house"""

    # A full house is 3 of a kind with a pair, so just using those functions in conjunction here.
    return is_three_kind(sorted_hand) and is_pair(sorted_hand)


def is_three_kind(sorted_hand):
    """ Function that returns true if sorted hand is three of a kind """

    # First, get the ranks of the cards in a list
    ranks = [card[0] for card in sorted_hand]
    three_kind = False

    # Then, iterate through sorted ranks and check if there are 3 of the same ranks
    for num in set(ranks):
        if ranks.count(num) == 3:
            three_kind = True
    return three_kind


def is_two_pair(sorted_hand):
    """ Function that returns true if sorted hand is two pair """

    # First, get the ranks of the cards in a list
    ranks = [card[0] for card in sorted_hand]

    # Then, use Counter class to create object with counts of each unique element in list,
    # and then sum the ones that have a count of 2
    num_counts = Counter(ranks)

    # If the sum is 2, there are two pairs and should return true
    pair_count = sum(count == 2 for count in num_counts.values())
    return pair_count == 2


def is_pair(sorted_hand):
    """ Function that returns true if sorted hand is a pair """

    # First, get the ranks of the cards in a list
    ranks = [card[0] for card in sorted_hand]
    pair = False

    # Then, iterate through sorted ranks and check if there are 4 of the same ranks
    for num in set(ranks):
        if ranks.count(num) == 2:
            pair = True
    return pair


def is_flush(sorted_hand):
    """ Function that returns true if sorted hand is a flush """

    # Check if the cards form a flush by seeing if the suits (second in the card tuple) all match
    flush = all(card[-1] == sorted_hand[0][-1] for card in sorted_hand)
    return flush


def is_straight(sorted_hand):
    """ Function that returns true if sorted hand is a straight """

    ranks = [card[0] for card in sorted_hand]
    # This is the only hand where an Ace being high or low is important, and only needs to be
    # converted to a value of 1 if at least a 2 is present in the list to be considered a
    # straight. Loop through the ranks that contain a 2 and if a 14 (A) is present, change it to
    # a value of 1. Then, resort the list
    if 2 in ranks:
        for index, value in enumerate(ranks):
            if value == 14:
                ranks[index] = 1
    ranks = sorted(ranks)

    # Check if cards are in consecutive order by first getting the ranks in a sorted list,
    # then using list comprehension to check if all elements in the list are consecutive,
    # and if all the elements are consecutive, the list comprehension will return a list of True
    # values; if not, the list will have at least one False value. Then use the all() function to
    # check that all the boolean values in the list are True. If all elements are True,
    # then it is a straight.
    return all(ranks[i] == ranks[i - 1] + 1 for i in range(1, len(ranks)))


def is_royal_flush(sorted_hand):
    """ Function that returns true if sorted hand is a royal flush """

    # Check if the cards form a flush
    flush = is_flush(sorted_hand)

    # Check if the cards are all face cards
    royal_flush_ranks = [10, 11, 12, 13, 14]
    royal_flush_condition = [card[0] in royal_flush_ranks for card in sorted_hand]

    # Check that it is a royal flush (which is true if it is a flush and the face cards are "royal")
    return flush and all(royal_flush_condition)


def is_straight_flush(sorted_hand):
    """ Function that returns true if sorted hand is a straight flush """

    # Check if the cards form a flush
    flush = is_flush(sorted_hand)

    # Check if numbers are consecutive (straight)
    straight = is_straight(sorted_hand)
    return flush and straight


def is_four_kind(sorted_hand):
    """ Function that returns true if sorted hand is four of a kind """

    # First, get the ranks of the cards in a list
    ranks = [card[0] for card in sorted_hand]
    four_kind = False

    # Then, iterate through sorted ranks and check if there are 4 of the same ranks
    for num in set(ranks):
        if ranks.count(num) == 4:
            four_kind = True
    return four_kind


def sort_cards(cards):
    """ Function to sort cards from low to high, input is a list of cards, output is a list"""

    # I am converting each card in the player's set of cards into a numeric value by calling my
    # convert_card_to_numeric function, and then sorting those values from low to high
    numeric_hand = [convert_card_to_numeric(card) for card in cards]
    sorted_cards = sorted(numeric_hand, key=lambda x: x[0])
    return sorted_cards


def hand_ranking(cards):
    """ Function that returns the hand as a string with input of a list of cards """

    # First, sort cards
    sorted_cards = sort_cards(cards)

    # Next, call on boolean functions that determine if the sorted cards are a specific hand or not.
    # Going in the order from the highest hand to the lowest so that the code exits out when the
    # highest hand is found--prevents something like royal flush called as a straight or a flush
    if is_royal_flush(sorted_cards):
        return "Royal Flush"

    if is_straight_flush(sorted_cards):
        return "Straight Flush"

    if is_four_kind(sorted_cards):
        return "Four of a Kind"

    if is_full_house(sorted_cards):
        return "Full House"

    if is_flush(sorted_cards):
        return "Flush"

    if is_straight(sorted_cards):
        return "Straight"

    if is_three_kind(sorted_cards):
        return "Three of a Kind"

    if is_two_pair(sorted_cards):
        return "Two Pair"

    if is_pair(sorted_cards):
        return "Pair"

    return "High Card"


# Part 2: Deal Cards and Determine Winner


def deal_cards(player_list):
    """ Function that deals a list of players 5 cards each and stores output in dictionary"""

    # Creating a dictionary of players that will hold their names as keys and cards as a value
    players = {}
    deck = Deck()
    deck.build()

    # For each player in the list given, will give random 5 cards, and then remove those cards
    # from the overall deck so they are not repeated in another player's cards. Then saving the
    # player name as the key and their cards as the associated value
    for player in player_list:
        player_cards = random.sample(deck.cards, k=5)
        for card in player_cards:
            deck.cards.remove(card)
        players[player] = player_cards

    # Returning the dictionary of players and their cards
    return players


# Create dictionary that has the hands as the keys and their "score" as the values. Set these scores
# from 1-10, with 10 being the best hand and 1 being the high card.
score_hands = {"Royal Flush": 10, "Straight Flush": 9, "Four of a Kind": 8, "Full House": 7,
               "Flush": 6, "Straight": 5,
               "Three of a Kind": 4, "Two Pair": 3, "Pair": 2, "High Card": 1}


def winner_is(players):
    """Function that returns list of strings with input of dictionary of players and their hands"""

    # Output is list of strings so winner can include multiple players that have the same hand

    # Create an empty dictionary called scores that will have the players as the keys and their
    # scores as the values
    scores = {}

    # Loop through dictionary items and call hand_ranking to determine that player's hand
    for player, hand in players.items():
        player_hand = hand_ranking(hand)

        # Get specific player's scores by referencing the pre-made dictionary called score_hands
        # Look up the player score in the dictionary by using their hand as key
        player_score = score_hands[player_hand]

        # Add that player and their score into the scores dictionary
        scores[player] = player_score

    # Find the max scores in the dictionary and see which of the players have that max score by
    # using list comprehension.
    max_scores = max(scores.values())
    winning_players = [player for player, score in scores.items() if score == max_scores]

    # Return list of winners
    return winning_players


# Part 3: OOP
class Card:
    """ Class representing a card """

    def __init__(self, suit, val):
        """ Initialize the card with its suit and value"""
        self.suit = suit
        self.val = val
        self.card = val + suit
        # Create tuple that represents the numeric value of the card by converting its rank to an
        # integer and separating out the suit as string
        self.num_card = ()

    def show(self):
        """ Function that returns the variable card that holds the value and the suit inputted
        when a card is created, i.e., shows a card"""
        return self.card

    def convert_card(self):
        """ Function that converts card to numeric version as a tuple """
        rank_str = self.val
        suit = self.suit

        # Making a dictionary with the face cards and their numeric values
        face_card_values = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}

        # If the rank is a face card, getting the associated numeric value of it and saving it to
        # a new variable, rank_numeric
        if rank_str in face_card_values:
            rank_numeric = face_card_values[rank_str]
        # Otherwise, converting the string rank into a numeric value
        else:
            rank_numeric = int(rank_str)

        self.num_card = (rank_numeric, suit)
        # Returning the card as a tuple of the integer rank and the string suit
        return self.num_card


class Deck:
    """ Class representing a deck """

    def __init__(self):
        """ Initialize deck """
        # Create empty list of cards that represents the deck. Populate this list with build()
        self.cards = []

    def show(self):
        """ Function to show the cards by returning list of cards"""
        return self.cards

    def build(self):
        """ Function that builds deck of 52 cards"""

        # Build this deck of cards by looping 4 times (once for each of the four suits) and
        # create 13 separate cards from 2-14 that correspond with the ranks. Account for the
        # face cards by making them 11-14.
        for suit in range(4):
            for num in range(2, 15):
                if num == 11:
                    num = "J"
                if num == 12:
                    num = "Q"
                if num == 13:
                    num = "K"
                if num == 14:
                    num = "A"

                if suit == 0:
                    card = str(num) + "h"
                    self.cards.append(card)
                if suit == 1:
                    card = str(num) + "d"
                    self.cards.append(card)
                if suit == 2:
                    card = str(num) + "c"
                    self.cards.append(card)
                if suit == 3:
                    card = str(num) + "s"
                    self.cards.append(card)

    def shuffle(self, num=1):
        """ Function that shuffles the list of cards in deck num amount of times """

        # Shuffle the cards in the deck by using the random.shuffle function, and looping
        # through a range of num to reflect the number of times the user wants to shuffle
        for _ in range(num):
            random.shuffle(self.cards)
        return self.cards

    def deal(self):
        """ Function that deals one card from deck """

        # Use pop to return the last card in the list of cards (should be done after the deck of
        # cards is shuffled) and remove that card from the deck by removing it from the list
        return self.cards.pop()


class Player:
    """ Class representing a player"""

    def __init__(self, name):
        """ Initialize player object with name"""
        self.name = name
        # Create empty list that will hold the player's cards
        self.player_cards = []

    def say_hello(self):
        """ Function that returns a hello statement with player name """

        # Use an f string to say hello and the player's name when the function is called
        return f"Hi, I'm {self.name}!"

    def draw(self, deck, num=1):
        """ Function that populates a player's cards with a num amount of cards from the deck """

        # If number of cards in the deck are greater or equal to the number of cards to draw,
        # then it is possible to draw the cards and return True.
        if len(deck.cards) >= num:
            # Use random.sample to select random num of cards in the deck
            self.player_cards = random.sample(deck.cards, k=num)
            # Loop through the player's cards and remove each one from the deck so there are no
            # repeats.
            for card in self.player_cards:
                deck.cards.remove(card)
            return True
        # If the number of cards to draw is greater than the number of cards remaining in the deck,
        # the function will return False
        return False

    def show_hand(self):
        """ Function that returns the list of the player cards and show their hand"""
        return self.player_cards
