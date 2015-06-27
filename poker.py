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
    incr = 0
    m = 1
    count = 1
    maxcount = 0
    best= []
    collection = hand+board
    collection.sort()
    collection = collection[::-1]
    output = ""
    #find a pair
    for i in range(0,len(collection)):
        
        if i < len(collection)-1 and collection[i][0] == collection[i+1][0]: #if the ranks are the same
            count += 1 
        elif count > 1:
            best.append(collection[i-count+1:i+1])
            output += "{0} match found {1}".format(count,collection[i-count+1:i+1])+"\n"
            c_score = 0 # used to weigh hand scores against each other check_score
            
            if count == maxcount == 2: #2 pair found
                b = float(best[0][0][0])
                c_score = 10**math.floor(math.log(b,10)+1)*((b%10)+1*(math.floor(math.log(b,10)))) 
                c_score += best[1][1][0]
                if c_score > score:
                    score = c_score
            
                    output += "2 pair found    {0}\n".format(score)
            elif maxcount == 0: # first pair found
                score = best[0][0][0] + 11
                output += "pair found    {0}\n".format(score)
            if count + maxcount == 5: output += "boat found\n"
            elif count == 3: 
                score = best[-1][0][0] + 512
                output += "found trips    {0}\n".format(score)
            elif count == 4: output += "found quads\n"

            if maxcount < count: maxcount = count
            count = 1
        # output += str(count)+"\n"

        # output += "incr={0}".format(incr)+"\n"


    return output

## test vars/funcs
top = 13 * 4 # top card to draw-1 * 4

def convert(*cards):
    c_cards = [] #converted cards
    for i in cards:
        c_cards.append((int(i[:-1]),i[-1]))
    return c_cards



def test(runs):
    f = open('pokertest.txt','w')
    for _ in range(runs):
        redraw()
        shuffle(drawn)
        find_test = drawn[0:7]
        find_test.sort()
        f.write("\n\n"+str(find_test)+"\n")
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
test(1000)







