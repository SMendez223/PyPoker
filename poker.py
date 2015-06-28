#!/usr/bin/python
from random import *
import itertools as iter
import copy
import math
SUIT =  ['♠','♥','♦','♣']

RANK = [2,3,4,5,6,7,8,9,10,11,12,13,14]
FACE = ['J','Q','K','A']
output = ""
deck = []
#shuffle(deck)
players = 9
loc = 0 # location within a deck
hands = []
class Card(object):
    def __init__(self,rank,suit):
        assert type(rank) == int
        assert type(suit) == str
        self.__rank__ = rank
        self.__suit__ = suit
    def getsuit(self):
        return self.__suit__
    #returns int 2-14
    def getrankval(self):
        return self.__rank__
    #returns str 2-10 then face card J-A
    def getrank(self):
        if self.getrankval() > 10:
            return str(FACE[self.getrankval()%10-1])
        if self.getrankval() == 1:
            return str(FACE[-1])
        return str(self.getrankval())
    def __str__(self):
        return self.getrank()+self.getsuit()
    def __repr__(self):
        return str(self)
    def __getitem__(self,key):
        if key == 0: return self.getrank()
        return self.getsuit()

class Hand(object):
    def __init__(self, hand):
        assert type(hand) == list
        self.hand = hand
        self.__original__ = copy.deepcopy(hand) #non sorted
        self.sort_rank()

    def sort_rank(self,r=True):
        self.hand = sorted(self.hand, key=lambda x: x.getrankval(), reverse=r)
    def sort_suit(self,r=True):
        self.hand = sorted(self.hand, key=lambda x: x[1], reverse=r)
    def get_orig(self):
        return self.__original__
    def cards(self):
        return self.hand
    def __len__(self):
        return len(self.hand)
    def __getitem__(self,key):
        return self.hand[key]
    def __str__(self):
        return str(self.hand)    
    def __repr__(self):
        return str(self)
    def __add__(self,other):
        if type(other) == Hand:
            return Hand(self.cards() + other.cards())
        if type(other) == Card:
            return Hand(self.cards() + [other])


def new_deck():
    global deck
    deck = []
    for suit in SUIT:
        for rank in RANK:
            deck.append(Card(rank,suit))
    #shuffle(deck)
#pos : position in the deck to pull a card from
#num : number of cards to pull
def draw(num, pos=0):
    c = deck[pos:pos+num]
    for i in c:
        deck.remove(i)
    return c
def deal():
    for i in range(0,players):
        hands.append([deck[i],deck[i+players]])
    #deck = deck[players*2]    

def find(hand,board):
    

    #the second dict in s_check will contain an array of indexes of rank repetitions
    f_check = {}

    best= []
    collection = hand+board
    hand.sort_rank()
    collection.sort_rank()

    name = "High card" #collection name
    score = 0
    count = 1
    maxcount = 0
    output = ""
    output +=  str(collection)+"\n"
    #find a pair
    temp_score = 0L # used to weigh hand scores against each other check_score
    temp_name = name
    for i in range(0,len(collection)):
        if i < len(collection)-1 and collection[i][0] == collection[i+1][0]: #if the ranks are the same
            count += 1 
        #only true if next card is not the same. count tells the number of consecutive cards
        elif count > 1: 

            output += "{0} match found {1}".format(count,collection[i-count+1:i+1])+"\n"
            
            
            if score < 13: # first pair found
                temp_score = long(collection[i-count+1].getrankval() + 11)
                #output += "pair found  {0}\n".format(collection[i-count+1:i+1])
                temp_name = "pair {}'s".format(collection[i-count+1].getrank())
            
            elif score < 32: #2 pair found
                b = best[0].getrankval()
                # 2pair scoring algorithm
                temp_score = long(10**math.floor(math.log(b,10)+1)*((b%10)+1*(math.floor(math.log(b,10)))))
                temp_score += collection[i-count+1].getrankval() #get Rank of pair in best
                # used to be sure score for 2 pair is lower than previous score (if already scored)
                temp_name = "2 "+temp_name+" {}'s".format(collection[i-count+1].getrank())

            

            if count + maxcount == 5: 
                temp_name = "boat"
                temp_score = long(collection[i-count+1].getrankval() + 512*2)
                if(len(best) == 4):
                    best = best[0:2]
                
            elif count == 3: 
                temp_score = long(collection[i-count+1].getrankval() + 512)

                temp_name = "trips"

            elif count == 4: 
                temp_name = "quads"

            if maxcount < count: maxcount = count

            if temp_score > score:
                score = temp_score
                name = temp_name
                best += collection[i-count+1:i+1]
            count = 1
        # output += str(count)+"\n"

        # output += "incr={0}".format(incr)+"\n"

    if score < 527:
            #flip sort to high->low
            # if the highest card in the straights rank -4 == the lowest rank its a straight
            # ex: [10 J Q K A] -> flip -> [A K Q J 10] -> s[0] - 4 == s[4] == 10 -> STRAIGHT
            # ex: [9 J Q K A] -> flip -> [A K Q J 9] -> s[0] - 4 != s[4]         -> NOT STRAIGHT :'(
            s = is_straight(collection)
            if s:
                temp_name = "straight {} -> {}".format(s[-1].getrank(),s[0].getrank())
                temp_score = long(526+s[4].getrankval())
            if temp_score > score:
                score = temp_score
                name = temp_name
                best = copy.deepcopy(s)
                best = best[::-1] #flip it to make it low -> high
    # ## FIND FLUSHES
    # for key in f_check:
    #     if len(f_check[key]) >= 5:
    #         temp_name = "flush"
    #         for i in range(0,len(f_check[key])-4):
    #             temp_score = ""
                
    #             for card in f_check[key][i:i+5]:
    #                 #digit sum the Ranks
    #                 temp_score += str(get_rank(card))
    #             temp_score = long(temp_score)
    #             s = is_straight(f_check[key][i:i+5])
    #             if s:
    #                 temp_name = "straight flush"
    #                 temp_score *= 100
    #                 print "{} {}".format(f_check[key][0],f_check[key][0][0] == 14)
    #                 if s[0][0] == 14:
    #                     temp_name =  "royal flush"
    #                     # temp_score = 2**80

    #             if temp_score > score:
    #                 score = temp_score
    #                 name = temp_name
    #                 best = f_check[key][i:i+5]
        
    
    for card in collection:
        if card not in best and len(best) < 5:
            best.append(card)
    if score == 0: score = best[0].getrankval()
    output += "found {}    {}\n{}\n".format(name,best,score)

    output += "score: {}\n".format(float(score))
    output += "\n\n"
    if name:
        return output,score
    return ""
def is_straight(hand):
    h = {}
    assert type(hand) == Hand
    for card in hand:
        if 14 == card.getrankval():
            hand += Card(1,card.getsuit())
            break
   #remove duplicate ranks
    for card in hand:
        h[card.getrankval()] = card
    hand = h.values()
    hand.sort()
    hand = Hand(hand)
    
    for i in range(0,len(hand)-4):
        if hand[i].getrankval() - 4 == hand[4+i].getrankval():
            if hand[i+4][0] == 1:
                pass
            # print hand[i:i+5]
            # print "{} - 4 = {}    {}".format(hand[i][0], hand[4][0], hand[i][0]-4 == hand[4+i][0])
            return hand[i:i+5]
    return


## test vars/funcs
top = 13 * 4 # top card to draw-1 * 4

def out(o):
    global output
    output += str(o)+"\n"
##Convert human friendly list card names into list of card objects
def convert(*card):
    cards = []
    for i in card:
        i = i.split(",")
        if i[0] in FACE:
            cards.append(Card(int(FACE.index(i[0])+11),i[1]))
        else: cards.append(Card(int(i[0]),i[1]))
    return cards


def test(runs):
    f = open('./testfind.txt','w')
    for i in range(runs):
        new_deck()
        global deck
        shuffle(deck)
        find_test = sorted(draw(7),key=lambda card: card[0])
        f.write(find(Hand(find_test[:2]),Hand(find_test[2:]))[0])
        # if not i%1000: print i
    f.close()

t_hands = convert(*"A,♦ 2,♣ 3,♥ 4,♦ 5,♦ 6,♣ 8,♥".split(" "))
t_boards = "12H 11H 14D 14S 14C".split(" ")
# print find(t_hands,t_boards)
drawn = []

test(100)







