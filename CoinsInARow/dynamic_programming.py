#Kyle Dahlin 2016

#Several dynamic programming algorithms. Most are presented in the context
#of a game-like situation.

#INPUT FILE: Input file is one line with integer coin values separated by spaces.

import sys
import os.path
from math import ceil

#This algorithm deals with the coins-in-a-row scenario. A row of coins is
#presented each with seperate weights, say 6 5 2 7 3 5. Two users, A and B each
#take turns choosing a coin off of one end of the line until there are no coins
#left. So if A chooses 6, then B can either choose 5 at the left hand side or
#5 on the right hand side. When there are no coins left the user with the
#highest total coin value is declared the winner. The optimal strategy in This
# game is the one where every choice by a player is designed to minimize the
# maximum value of their opponent. This can be solved by the given algorithm below
# where every choice is made by assuming the opponent plays optimally as well.


#Function that reads from a file and collects the input. This will call the
# "optimal" function.
def find_optimal(filename):
    values = []
    #read the values from the file and convert them to integers
    with open(filename) as f:
        values = f.readline().strip().split(" ")
    values = list(map(lambda x: int(x), values))

    #2d array that contains the value that results from that optimal choice
    #at a subset of the values from index 1 to index 2
    memo = [[None]*len(values) for i in range(len(values))]

    optimal_value = optimal(0, len(values) - 1, values, memo)

    print("The optimal value with the given input is: {}".format(optimal_value))



#Function will compute the max value that can be obtained from
#index i to index j in a given list of coin values. This is done
#by comparing the value of choosing i and computing the value of the rest of the
# game going forward with that choice, or the choosing j and going forward. Each
# of these two scenarios is the value of the opponent playing optimally after you
# make a choice, which is minimized according to the description above. We can
#use memoization to store values from index i to j that we have already computed.

#Values = list of coins, i = beginning index, j = ending index
#memo = memoization table
def optimal(i, j, values, memo):
    #value is already computed, return
    if memo[i][j] != None:
        return memo[i][j]
    #the subset is one number, and is the optimal choice
    elif i == j:
        memo[i][j] = values[i]
    #subset is two numbers, optimal choice is the max
    elif i+1 == j:
        memo[i][j] = max(values[i], values[j])
    else:
        #these next two values assume that whatever choice is made, the opponent
        #will take that into consideration and play optimally as well. For example
        #in the case that i is chosen, the next choice that the same player can make
        #will either be the list after the opponent has chosen the value at J, or the
        #value at i + 1. Because they are playing optimally as well, we can assume
        #they take the one that gives them a higher value,
        choose_i = values[i] + min(optimal(i + 1, j - 1, values, memo), optimal(i + 2, j, values, memo))
        choose_j = values[j] + min(optimal(i, j - 2, values, memo), optimal(i + 1, j - 1, values, memo))
        memo[i][j] = max(choose_i, choose_j)

    return memo[i][j]


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("A file name was not specified, exiting")
        sys.exit()
    if not os.path.isfile(sys.argv[1]):
        print("The file specified does not exist, exiting")
        sys.exit()
    find_optimal(sys.argv[1])
