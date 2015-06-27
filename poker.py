#!/usr/bin/python
from random import *
import itertools as iter
import copy
import math
SUIT =  ['S','C','D','H']
RANK = [2,3,4,5,6,7,8,9,10,11,12,13,14]
MODEL_DECK = list(iter.product(RANK,SUIT))


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
    score = 0
    count = 1
    maxcount = 0

    #the second dict in s_check will contain an array of indexes of rank repetitions
    s_check = [{},{}] # [{Rank: index},{Rank: [other indexes]}]
    f_check = {}

    best= []
    collection = hand+board
    collection.sort()
    collection = collection[::-1]
    name = "" #collection name

    output = "\n\n"+str(collection)+"\n"
    #find a pair
    temp_score = 0 # used to weigh hand scores against each other check_score
    temp_name = name
    for i in range(0,len(collection)):

        if i < len(collection)-1 and collection[i][0] == collection[i+1][0]: #if the ranks are the same
            count += 1 
        #only true if next card is not the same. count tells the number of consecutive cards
        elif count > 1: 

            output += "{0} match found {1}".format(count,collection[i-count+1:i+1])+"\n"
            
            
            if score < 13: # first pair found
                temp_score = collection[i-count+1][0] + 11
                #output += "pair found  {0}\n".format(collection[i-count+1:i+1])
                temp_name = "pair"
            
            elif score < 32: #2 pair found
                b = float(collection[i-count+1][0])
                # 2pair scoring algorithm
                temp_score = 10**math.floor(math.log(b,10)+1)*((b%10)+1*(math.floor(math.log(b,10)))) 
                temp_score += best[0][0][0] #get Rank of pair in best
                # used to be sure score for 2 pair is lower than previous score (if already scored)
                temp_name = "2 pair"

            

            if count + maxcount == 5: 
                name = "boat"
                best.append(collection[i-count+1:i+1])
            
            elif count == 3: 
                temp_score = collection[i-count+1][0] + 512
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

        # if rank of card is not already in s_check[0] 
        if collection[i][0] not in s_check[0].keys():
            #if card is ace add it as 1 and 14
            if collection[i][0] == 14:
                s_check[0][1] = collection[i]
            s_check[0][collection[i][0]] = collection[i]

        else:
            #if the rank is not already a repetition (it only will be in case of count > 2)
            if collection[i][0] not in s_check[1].keys():
                #make a space for the card
                s_check[1][collection[i][0]] = []
            # add the card as repeated
            s_check[1][collection[i][0]].append(collection[i])

        #if the suit is a repetition store it
        if collection[i][1] not in f_check.keys():
            f_check[collection[i][1]] = []
        f_check[collection[i][1]].append(collection[i])

    if len(s_check[0]) >= 5 and score < 527:
        for i in range(0,len(s_check[0])-4):
            s = s_check[0].keys()
            s.sort()
            s = s[::-1][i:i+5] #flip sort to high->low
            # if the highest card in the straights rank -4 == the lowest rank its a straight
            # ex: [10 J Q K A] -> flip -> [A K Q J 10] -> s[0] - 4 == s[4] == 10 -> STRAIGHT
            # ex: [9 J Q K A] -> flip -> [A K Q J 9] -> s[0] - 4 != s[4]         -> NOT STRAIGHT :'(
            if s[0]-4 == s[4]:
                temp_name = "straight"
                temp_score = 526+s[4]
            if temp_score > score:
                score = temp_score
                name = temp_name
                best = []
                for key in s:
                     best.append(s_check[0][key])
                best = best[::-1] #flip it to make it low -> high
    ## FIND FLUSHES
    for key in f_check:
        if len(f_check[key]) >= 5:
            temp_name = "flush"
            for i in range(0,len(f_check[key])-4):
                temp_score = ""
                for card in f_check[key][i:i+5]:
                    temp_score += str(get_rank(card))
                temp_score = int(temp_score)

                if f_check[key][i:i+5][0][0] - 4 == f_check[key][i:i+5][4][0]:
                    temp_name = "straight flush"
                    temp_score *= 1000

                if temp_score > score:
                    score = temp_score
                    name = temp_name
                    best = f_check[key][i:i+5]

    output += "found {}    {}\n".format(name,best)
    output += "score: {}\n".format(float(score))
    if "flush" in name:
        return output
    return ""
def get_rank(card):
    assert type(card) == tuple
    return card[0]


## test vars/funcs
top = 13 * 4 # top card to draw-1 * 4

def convert(*cards):
    c_cards = [] #converted cards
    for i in cards:
        c_cards.append((int(i[:-1]),i[-1]))
    return c_cards



def test(runs):
    f = open('./testfind.txt','w')
    for _ in range(runs):
        redraw()
        shuffle(drawn)
        find_test = drawn[0:7]
        find_test.sort()
        f.write(find(find_test[:2],find_test[2:]))
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







