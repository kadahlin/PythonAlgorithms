#Kyle Dahlin

#This program implements a greedy strategy for maximizing the value of a set of
# items with a weight constraint. The input set is a list of items each with a
# positive weight and a total benefit. The goal is to find a set of items that can
# fit in a fictional "knapsack" or collection that has a total weight W. The algorithm
# will filter through this list of items and assign values to each item. The value
# of an item is the benefit/weight of each item, so we giving priority to the items
# that have the most value in order to maximize the total value of our collection.

# This is the fractional knapsack, as opposed to the 0-1 knapsack problem, because
# we are allowed to only take portions of the items. For example if the item "x" with
# the most value weighs 10 units but our knapsack only has the capacity of 5 units,
# we can take half of item x.

#INPUT FILE: a text file where each line is an item weight and an item benefit,
#separated by a tab character.

import sys
import os.path

def fractional_knapsack(filename):
    #Dictionary with integer keys denoting the order they appeared in the INPUT
    #list and tuple values with are the items weights combined with the benefits.
    #The item order does not matter but I included it to output the solution
    #nicely.
    items = {}
    index = 0
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            if index == 0:  #First line should just contain the weight
                weight = int(line.strip())
                index += 1
                continue
            pair = line.strip().split('\t')
            items[index] = (int(pair[0]), int(pair[1]))
            index += 1
    #The items are sorted by their value which is given by the benefit / weight.
    sorted_items = sorted(items, key=lambda kv: items[kv][1]/items[kv][0], reverse=True)
    weigh_benefits(weight, sorted_items, items)


#Sorted_items is the list of keys in the dict ordered by decreasing value, and items is
#the dictionary containing the items paired with their benefits and weights.
def weigh_benefits(weight, sorted_items, items):
    current_weight = 0
    while current_weight < weight and sorted_items != []:
        #Remove the highest value item from the list.
        item = sorted_items[0]
        sorted_items = sorted_items[1:]
        #This is the amount of the current item that we have room for. By checking
        #the weight - current_weight we can ensure that we will never overflow
        #the total weight.
        fraction = min(items[item][0], weight - current_weight)
        current_weight += fraction
        print("{} of item {}".format(fraction, item))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("A filename was not specified, exiting.")
        sys.exit()
    if not os.path.isfile(sys.argv[1]):
        print("Could not see the specified file, exiting.")
        sys.exit()
    fractional_knapsack(sys.argv[1])
