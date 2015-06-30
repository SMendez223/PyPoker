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
    def getSuit(self):
        return self.__suit__
    #returns int 2-14
    def getValue(self):
        return self.__rank__
    #returns str 2-10 then face card J-A
    def getRank(self):
        if self.getValue() > 10:
            return str(FACE[self.getValue()%10-1])
        if self.getValue() == 1:
            return str(FACE[-1])
        return str(self.getValue())
    def __str__(self):
        return self.getRank()+self.getSuit()
    def __repr__(self):
        return str(self)
    def __getitem__(self,key):
        if key == 0: return self.getRank()
        return self.getSuit()



class Hand(object):
    def __init__(self, hand=[]):
        assert type(hand) == list
        self.hand = hand
        self.__original__ = copy.deepcopy(hand) #non sorted
        self.sort_rank()

        # High Card, Pair, 2 pair, etc
        self.collection_name = ""
    def sort_rank(self,r=True):
        self.hand = sorted(self.hand, key=lambda x: x.getValue(), reverse=r)
    def sort_suit(self,r=True):
        self.hand = sorted(self.hand, key=lambda x: x[1], reverse=r)
    def getOrig(self):
        return self.__original__
    def cards(self):
        return self.hand
    def __len__(self):
        return len(self.hand)
    def __getitem__(self,key):
        return self.hand[key]
    def __str__(self):
        return str(type(self))+" "+str(self.hand)    
    def __repr__(self):
        return str(self)
    def __add__(self,other):
        if type(other) == Hand:
            return Hand(self.cards() + other.cards())
        if type(other) == Card:
            return Hand(self.cards() + [other])
        if type(other) == list:
            return Hand(self.cards() + other)

class RankedHand(object):
    def __init__(self, best, kickers, name, score):
        assert type(best) == type(kickers) == list
        self._best = best
        self._kickers = kickers
        self._name = name
        self._score = score
    def name(self):
        return self.collection_name
    def best(self):
        return self._best
    def kickers(self):
        return self._kickers
    def name(self):
        return self._name
    def score(self):
        return self._score
    def cards(self):
        return self.best() + self.kickers()
    def __str__(self):
        return self.name()+" "+str(self.cards())+" "+str(self.score())    
    def __repr__(self):
        return str(self)


# class Player(object):
#     """docstring for Player"""
#     id = 1
#     def __init__(self, hand):

#         self.arg = arg
        
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
    f_check = []
    best= []
    collection = hand+board
    name = "High card" #collection name
    score = 0
    count = 1
    maxcount = 0
    output = ""
    output +=  str(collection)+"\n"

    temp_best = []
    #find a pair
    temp_score = 0L # used to weigh hand scores against each other check_score
    temp_name = name
    
    if score < 527:
        #flip sort to high->low
        # if the highest card in the straights rank -4 == the lowest rank its a straight
        # ex: [10 J Q K A] -> flip -> [A K Q J 10] -> s[0] - 4 == s[4] == 10 -> STRAIGHT
        # ex: [9 J Q K A] -> flip -> [A K Q J 9] -> s[0] - 4 != s[4]         -> NOT STRAIGHT :'(
        s = is_straight(collection)
        if s:
            temp_name = "straight {} -> {}".format(s[-1].getRank(),s[0].getRank())
            temp_score = long(526+s[4].getValue())
        if temp_score > score:
            score = temp_score
            name = temp_name
            best = copy.deepcopy(s)
            best = best[::-1] #flip it to make it low -> high
    for i in range(0,len(collection)):
        
        if i < len(collection)-1 and collection[i][0] == collection[i+1][0]: #if the ranks are the same
            count += 1 
        #only true if next card is not the same. count tells the number of consecutive cards
        elif count > 1: 
            temp_best = collection[i-count+1:i+1]
            output += "{0} match found {1}".format(count,collection[i-count+1:i+1])+"\n"
            
            
            if score < 13: # first pair found
                temp_score = long(temp_best[0].getValue() + 11)
                #output += "pair found  {0}\n".format(collection[i-count+1:i+1])
                temp_name = "pair {}'s".format(temp_best[0].getRank())
            
            elif score < 32: #2 pair found
                b = best[0].getValue()
                # 2pair scoring algorithm
                temp_score = long(10**math.floor(math.log(b,10)+1)*((b%10)+1*(math.floor(math.log(b,10)))))
                temp_score += temp_best[0].getValue() #get Rank of pair in best
                # used to be sure score for 2 pair is lower than previous score (if already scored)
                temp_name = "2 "+temp_name+" {}'s".format(temp_best[0].getRank())

            


            if count == 3: 
                temp_score = long(temp_best[0].getValue() + 512)
                temp_name = "trip {}'s".format(temp_best[0].getRank())
                if(len(best) == 4):
                    best = best[0:2]
            if count + maxcount == 5: 
                temp_name = "{}'s full of {}"
                temp_score -= 512 # rank of trips
                temp_score *= 1000
                if count == 2:
                    temp_name = temp_name.format(best[0].getRank(), temp_best[0].getRank())
                    temp_score += temp_best[0].getValue()
                if count == 3:
                    temp_name = temp_name.format(temp_best[0].getRank(), best[0].getRank())
                    temp_score += best[0].getValue()
                temp_score += 200000000 # highest flush is 141,312,119

                
                
            

            elif count == 4: 
                temp_name = "quad {}'s".format(temp_best[0].getRank())
                temp_score = temp_best[0].getValue() + 300000000

            if maxcount < count: maxcount = count

            if temp_score > score:
                score = temp_score
                name = temp_name
                best += collection[i-count+1:i+1]
            count = 1
        # output += str(count)+"\n"

        # output += "incr={0}".format(incr)+"\n"


    # FIND FLUSHES
    collection.sort_suit()
    count = 0
    for i in range(len(collection)-4):
        if collection[i-count].getSuit() == collection[i+4].getSuit(): 
            f_check = collection[i-count:i+5]
            count += 1
            temp_name = "flush"
            temp_score = ""
   
    if f_check:
        s = is_straight(Hand(f_check))
        if s:
            temp_name = "straight flush"
            temp_score = "1000"
            f_check = copy.deepcopy(s)
            if s[0].getValue() == 14:
                temp_name = "Royal Flush"

        for card in f_check:
            temp_score += str(card.getValue())
        temp_score = long(temp_score)
        if temp_score > score:
            score = temp_score
            name = temp_name
            best = f_check  

    

    ##find highest 5 card hand
    temp_best = copy.deepcopy(best)
    kickers = []
    collection.sort_rank()
    for card in collection:
        if card not in best and len(best)+len(kickers) < 5:
            kickers.append(card)

    ##if the best hand uses all five cards on the board
    ##your REAL score is 0
    if len(set(board) - set(best + kickers)) == 0:
        score = -1



    output += "found {}    {}\n{}\n".format(name,best,score)
    output += "score: {}\n".format(long(score))
    output += "\n\n"
    if name:
        return RankedHand(best,kickers,name,score)
    return ""

def showdown(board,*players):
    assert type(players) == Player
    maxscore = 0
    maxhands = []
    for player in players:
        if player.getScore() > maxscore:
            maxscore = score
            maxhands = [player]
        elif player.getScore() == maxscore:
            maxhands.append(player)
    for player in maxhands:
        #if players hand is being used in the best hand
        if set(player.getKickers()) >= set(player.getHand()):
            pass



def is_straight(hand):
    h = {}
    assert type(hand) == Hand
    for card in hand:
        if 14 == card.getValue():
            hand += Card(1,card.getSuit())
            break
   #remove duplicate ranks
    for card in hand:
        h[card.getValue()] = card
    hand = h.values()
    hand.sort()
    hand = Hand(hand)
    
    for i in range(0,len(hand)-4):
        if hand[i].getValue() - 4 == hand[4+i].getValue():
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


def test():
    f = open('./testfind.txt','w')
    for i in range(len(t_hands)):
        f.write(find(Hand(t_hands[i]),Hand(t_boards[i]))[0])
        if not i%1000: print i
    f.close()
def testrand(runs):
    f = open('./testfind.txt','w')
    for i in range(runs):
        new_deck()
        global deck
        shuffle(deck)
        find_test = sorted(draw(7),key=lambda card: card[0])
        f.write(find(Hand(find_test[:2]),Hand(find_test[2:]))[0])
        if not i%1000: print i
    f.close()
def test_showdown(runs,players):
    """will simulate a showdown between players, and choose a winner"""
    f = open('./testfind.txt','w')
    global deck
    for _ in range(runs):
        hands = []
        scores = []
        new_deck()
        shuffle(deck)
        board = Hand(draw(5))
        f.write(str(board)+"\n")
        for i in range(players):
            p = find(Hand(draw(2)),board)
            f.write("Player {}: {} {}\n".format(i+1,p.cards(),p.name()))
        f.write("\n\n")
    f.close()
t_hands = [convert(*"A,♦ 10,♦".split(" "))]
t_boards = [convert(*"J,♦ Q,♦ K,♦ 9,♦ 8,♦".split(" "))]
# print find(t_hands,t_boards)
drawn = []

test_showdown(100,4)

new_deck()
shuffle(deck)
hand = Hand(draw(2))
board = Hand(draw(5))
best= find(hand,board)






