import random
from collections import Counter


# Part 1: Poker Hands

# First, I want a function that converts a player's cards in a sorted hand, with the face cards having inherent
# numeric values
def convert_card_to_numeric(card):
    # Getting the rank of the card which will initially be a string by getting everything but the last element in the
    # string which will be the suit
    rank_str = card[:-1]
    suit = card[-1]

    # Making a dictionary with the face cards and their numeric values
    face_card_values = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    # If the rank is a face card, getting the associated numeric value of it and saving it to a new variable,
    # rank_numeric
    if rank_str in list(face_card_values.keys()):
        rank_numeric = face_card_values.get(rank_str)
    # Otherwise, converting the string rank into a numeric value
    else:
        rank_numeric = int(rank_str)

    # Returning the card as a tuple of the integer rank and the string suit
    return rank_numeric, suit


# In order to accomplish this, creating distinct functions that will determine if a player's sorted cards belong to
# one of the 10 different hands in poker

def is_full_house(sorted_hand):
    # A full house is 3 of a kind with a pair, so just using those functions in conjunction here.
    # If they are both true, it is a full house
    return is_three_kind(sorted_hand) and is_pair(sorted_hand)


def is_three_kind(sorted_hand):
    # First, get the ranks of the cards in a list
    ranks = [card[0] for card in sorted_hand]
    three_kind = False

    # Then, iterate through sorted ranks and check if there are 3 of the same ranks
    for num in set(ranks):
        if ranks.count(num) == 3:
            three_kind = True
    return three_kind


def is_two_pair(sorted_hand):
    # First, get the ranks of the cards in a list
    ranks = [card[0] for card in sorted_hand]

    # Then, use Counter class to create object with counts of each unique element in list, and then sum the ones that
    # have a count of 2
    num_counts = Counter(ranks)

    # If the sum is 2, there are two pairs and should return true
    pair_count = sum(count == 2 for count in num_counts.values())
    return pair_count == 2


def is_pair(sorted_hand):
    # First, get the ranks of the cards in a list
    ranks = [card[0] for card in sorted_hand]
    pair = False

    # Then, iterate through sorted ranks and check if there are 4 of the same ranks
    for num in set(ranks):
        if ranks.count(num) == 2:
            pair = True
    return pair


def is_flush(sorted_hand):
    # Check if the cards form a flush by seeing if the suits all match
    flush = all(card[-1] == sorted_hand[0][-1] for card in sorted_hand)
    return flush


def is_straight(sorted_hand):
    ranks = [card[0] for card in sorted_hand]
    # This is the only hand where an Ace being high or low is important, and only needs to be converted to a value of
    # 1 if at least a 2 is present in the list to be considered a straight. Loop through the ranks that contain a 2
    # and if a 14 (A) is present, change it to a value of 1. Then, resort the list
    if 2 in ranks:
        for i in range(len(ranks)):
            if ranks[i] == 14:
                ranks[i] = 1
    ranks = sorted(ranks)
    # Check if cards are in consecutive order by first getting the ranks in a sorted list, then using list
    # comprehension to check if all elements in the list are consecutive, and if all the elements are consecutive,
    # the list comprehension will return a list of True values; if not, the list will have at least one False value.
    # Then use the all() function to check that all the boolean values in the list are True. If all elements are
    # True, then it is a straight.
    return all(ranks[i] == ranks[i - 1] + 1 for i in range(1, len(ranks)))


def is_royal_flush(sorted_hand):
    # Check if the cards form a flush
    flush = is_flush(sorted_hand)

    # Check if the cards are all face cards
    royal_flush_ranks = [10, 11, 12, 13, 14]
    royal_flush_condition = [card[0] in royal_flush_ranks for card in sorted_hand]

    # Check that it is a royal flush (which is true if it is a flush and the face cards are "royal")
    return flush and all(royal_flush_condition)


def is_straight_flush(sorted_hand):
    # Check if the cards form a flush
    flush = is_flush(sorted_hand)

    # Check if numbers are consecutive (straight)
    straight = is_straight(sorted_hand)
    return flush and straight


def is_four_kind(sorted_hand):
    # First, get the ranks of the cards in a list
    ranks = [card[0] for card in sorted_hand]
    four_kind = False

    # Then, iterate through sorted ranks and check if there are 4 of the same ranks
    for num in set(ranks):
        if ranks.count(num) == 4:
            four_kind = True
    return four_kind


def sort_cards(cards):
    # I am converting each card in the player's set of cards into a numeric value by calling my
    # convert_card_to_numeric function, and then sorting those values from low to high
    numeric_hand = [convert_card_to_numeric(card) for card in cards]
    sorted_cards = sorted(numeric_hand, key=lambda x: x[0])
    return sorted_cards


def hand_ranking(cards):
    sorted_cards = sort_cards(cards)
    # I am calling on the boolean functions I wrote earlier that determine if the sorted cards are a hand or
    # not. I am going in the order from the highest hand to the lowest so that the code exits out when the highest
    # hand is found. This prevents something like a royal flush being called as a straight or a flush
    if is_royal_flush(sorted_cards):
        return "Royal Flush"

    elif is_straight_flush(sorted_cards):
        return "Straight Flush"

    elif is_four_kind(sorted_cards):
        return "Four of a Kind"

    elif is_full_house(sorted_cards):
        return "Full House"

    elif is_flush(sorted_cards):
        return "Flush"

    elif is_straight(sorted_cards):
        return "Straight"

    elif is_three_kind(sorted_cards):
        return "Three of a Kind"

    elif is_two_pair(sorted_cards):
        return "Two Pair"

    elif is_pair(sorted_cards):
        return "Pair"

    else:
        return "High Card"


# Part 2: Deal Cards and Determine Winner
def deal_cards(player_list):
    # Creating a dictionary of players that will hold their names as keys and cards as a value
    players = {}
    deck = Deck()
    deck.build()
    # For each player in the list given, will give random 5 cards, and then remove those cards from the overall deck
    # so they are not repeated in another player's cards. Then saving the player name as the key and their cards as
    # the associated value
    for player in player_list:
        player_cards = random.sample(deck.cards, k=5)
        for card in player_cards:
            deck.cards.remove(card)
        players[player] = player_cards

    # Returning the dictionary of players and their cards
    return players


# I created a dictionary that has the hands as the keys and their "score" as the values. I've set these scores from
# 1-10, with 10 being the best hand and 1 being the high card.
score_hands = {"Royal Flush": 10, "Straight Flush": 9, "Four of a Kind": 8, "Full House": 7, "Flush": 6, "Straight": 5,
               "Three of a Kind": 4, "Two Pair": 3, "Pair": 2, "High Card": 1}


# For the winner_is function, I am actually returning a list of strings instead of a string that includes multiple
# players that have the same hand, and that is the winning hand
def winner_is(round):
    # I've created an empty dictionary called scores that will have hte players as the keys and their scores as the
    # values
    scores = {}

    # I am looping through the items in the round dictionary that has the players and their associated cards as the
    # values and calling hand_ranking to determine that player's hand based on their cards
    for player, hand in round.items():
        player_hand = hand_ranking(hand)
        # Then, I get that player's scores by referencing the premade dictionary called score_hands  I am looking up
        # the player score in the dictionary by calling their hand as the key.
        player_score = score_hands[player_hand]

        # Then, I am adding that player and their score into the scores dictionary
        scores[player] = player_score
    # I am finding the max scores in the dictionary and seeing which of the players have that max score by using list
    # comprehension. I am then returning that list
    max_scores = max(scores.values())
    winning_players = [player for player in scores if scores[player] == max_scores]
    return winning_players


# TODO: If I had time, I would add an additional function/functions to determine who is the winner when multiple
#  players have the same hand
#  def tie_breaker(winning_players):
#  pass


# Part 3: OOP
class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.val = val
        self.card = val + suit
        # I have created an additional variable here, a tuple that represents the numeric value of the card by
        # converting its rank to an integer and separating out the suit
        self.num_card = ()

    # To show the card, I am returning the variable card that is the value and the suit that is inputted when a card
    # is created
    def show(self):
        return self.card

    # I want to include my convert to numeric version of the card function here
    def convertCard(self):
        rank_str = self.val
        suit = self.suit

        # Making a dictionary with the face cards and their numeric values
        face_card_values = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}

        # If the rank is a face card, getting the associated numeric value of it and saving it to a new variable,
        # rank_numeric
        if rank_str in list(face_card_values.keys()):
            rank_numeric = face_card_values.get(rank_str)
        # Otherwise, converting the string rank into a numeric value
        else:
            rank_numeric = int(rank_str)

        self.num_card = (rank_numeric, suit)
        # Returning the card as a tuple of the integer rank and the string suit
        return self.num_card


class Deck:
    def __init__(self):
        # I've created an empty list of cards that represents the deck. I will populate this list when I call build()
        self.cards = []

    def show(self):
        # To show the cards, I am just calling a print function that prints the list cards that is a variable of this
        # class
        return self.cards

    # I am building this deck of cards by looping 4 times (once for each of the four suits) and creating 13
    # separate cards from 2-14 that correspond with the ranks. I've accounted for the face cards by making them
    # 11-14. I've done this by looping again in a range of 2-15
    def build(self):
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

    # I am shuffling the cards in the deck by using the random.shuffle function, and looping through a range of num
    # to reflect the number of times the user wants to shuffle
    def shuffle(self, num=1):
        for i in range(num):
            random.shuffle(self.cards)
        return self.cards

    # To deal one card, I am using pop to return the last card in the list of cards (this should be done after the
    # deck of cards is shuffled) and remove that card from the deck by removing it from the list
    def deal(self):
        return self.cards.pop()


class Player:
    def __init__(self, name):
        # The two variables here are name, which should be inputted when the user creates a player and an empty list
        # that will hold the player's cards
        self.name = name
        self.player_cards = []

    # I am using an f string to say hello and the player's name when the function is called
    def sayHello(self):
        return f"Hi, I'm {self.name}!"

    # The two parameters for this function are the deck of cards and the number of cards to draw. If the number of
    # cards in the deck are greater or equal to the number of cards to draw, then it is possible to draw the cards. I
    # used random.sample to select num of cards in the deck, and then I am looping through the player's cards and
    # removing each one from the deck so there are no repeats. If the number of cards to draw is greater than the
    # number of cards remaining in the deck, the function will return False
    def draw(self, deck, num=1):
        if len(deck.cards) >= num:
            self.player_cards = random.sample(deck.cards, k=num)
            for card in self.player_cards:
                deck.cards.remove(card)
        else:
            return False

    # To show the player's hand, I am returning the list of the player cards
    def showHand(self):
        return self.player_cards
