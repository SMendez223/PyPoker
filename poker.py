#!/usr/bin/python
from random import *
import itertools as iter
import copy
import math
SUIT =  ['S','C','D','H']
RANK = [2,3,4,5,6,7,8,9,10,11,12,13,14]
MODEL_DECK = list(iter.product(RANK,SUIT))

output = ""
deck = copy.deepcopy(MODEL_DECK)
#shuffle(deck)
players = 9
loc = 0 # location within a deck
hands = []

def new_deck():
    global deck
    deck = copy.deepcopy(MODEL_DECK)
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
    score = 0L
    count = 1
    maxcount = 0

    #the second dict in s_check will contain an array of indexes of rank repetitions
    f_check = {}

    best= []
    collection = hand+board
    collection.sort()
    collection = collection[::-1]
    name = "" #collection name

    output = "\n\n"+str(collection)+"\n"
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
                temp_score = long(collection[i-count+1][0] + 11)
                #output += "pair found  {0}\n".format(collection[i-count+1:i+1])
                temp_name = "pair"
            
            elif score < 32: #2 pair found
                b = float(collection[i-count+1][0])
                # 2pair scoring algorithm
                temp_score = long(10**math.floor(math.log(b,10)+1)*((b%10)+1*(math.floor(math.log(b,10)))))
                temp_score += best[0][0][0] #get Rank of pair in best
                # used to be sure score for 2 pair is lower than previous score (if already scored)
                temp_name = "2 pair"

            

            if count + maxcount == 5: 
                name = "boat"
                best.append(collection[i-count+1:i+1])
            
            elif count == 3: 
                temp_score = long(collection[i-count+1][0] + 512)
                temp_name = "trips"

            elif count == 4: 
                temp_name = "quads"

            if maxcount < count: maxcount = count

            if temp_score > score:
                score = temp_score
                name = temp_name
                best.append(collection[i-count+1:i+1])
            count = 1
        # output += str(count)+"\n"

        # output += "incr={0}".format(incr)+"\n"

        #FLUSH SETUP
        #if the suit is a repetition store it
        if collection[i][1] not in f_check.keys():
            f_check[collection[i][1]] = []
        f_check[collection[i][1]].append(collection[i])

    if score < 527:
            #flip sort to high->low
            # if the highest card in the straights rank -4 == the lowest rank its a straight
            # ex: [10 J Q K A] -> flip -> [A K Q J 10] -> s[0] - 4 == s[4] == 10 -> STRAIGHT
            # ex: [9 J Q K A] -> flip -> [A K Q J 9] -> s[0] - 4 != s[4]         -> NOT STRAIGHT :'(
            s = is_straight(collection)
            if s:
                temp_name = "straight"
                temp_score = long(526+s[4][0])
            if temp_score > score:
                score = temp_score
                name = temp_name
                best = copy.deepcopy(s)
                best = best[::-1] #flip it to make it low -> high
    ## FIND FLUSHES
    for key in f_check:
        if len(f_check[key]) >= 5:
            temp_name = "flush"
            for i in range(0,len(f_check[key])-4):
                temp_score = ""
                
                for card in f_check[key][i:i+5]:
                    #digit sum the Ranks
                    temp_score += str(get_rank(card))
                temp_score = long(temp_score)
                s = is_straight(f_check[key][i:i+5])
                if s:
                    temp_name = "straight flush"
                    temp_score *= 100
                    print "{} {}".format(f_check[key][0],f_check[key][0][0] == 14)
                    if s[0][0] == 14:
                        temp_name =  "royal flush"
                        # temp_score = 2**80

                if temp_score > score:
                    score = temp_score
                    name = temp_name
                    best = f_check[key][i:i+5]
    best.sort()
    output += "found {}    {}\n".format(name,best)
    output += "score: {}\n".format(float(score))
    if "straight" in name:
        return output
    return ""
def get_rank(card):
    assert type(card) == tuple
    return card[0]
#hand is list of cards

def is_straight(hand):
    h = {}
    assert type(hand) == list
    for card in hand:
        if 14 in card:
            hand.append((1,card[1]))
            break
   #remove duplicate ranks
    for card in hand:
        h[card[0]] = card
    hand = h.values()
    hand.sort()
    hand = hand[::-1]
    
    for i in range(0,len(hand)-4):
        if hand[i][0] - 4 == hand[4+i][0]:
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
def convert(*cards):
    c_cards = [] #converted cards
    for i in cards:
        c_cards.append((int(i[:-1]),i[-1]))
    return c_cards



def test(runs):
    f = open('./testfind.txt','w')
    for i in range(runs):
        redraw()
        shuffle(drawn)
        find_test = drawn[0:7]
        find_test.sort()
        f.write(find(find_test[:2],find_test[2:]))
        if not i%1000: print i
    f.close()

t_hands = convert(*"13H 14H".split(" "))
t_boards = convert(*"12H 11H 14D 14S 14C".split(" "))

# print find(t_hands,t_boards)
drawn = []
def redraw():
    new_deck()
    global drawn
    drawn = draw(top)
test(100000)







