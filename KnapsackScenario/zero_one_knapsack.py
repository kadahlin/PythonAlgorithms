#Kyle Dahlin

#INPUT FILE: a text file where each line is an item weight and an item benefit,
#separated by a tab character.

# The running time of the algorithm is O(nW) where n is the number of items in the
# input list and W is the total weight that can be contained in the knapsack.


import sys
import os.path

def zero_one_knapsack(filename):
    #Each key in the dict the integer of the index in the file and the values
    #are the weights paired with the benefits. Value is found by value/weight.
    items = {}
    index = 0;
    weight = 0;
    #Add the input to the data structures
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
    #Memoization table
    table = [[0]*(weight+1) for i in range(index)]
    for i in range(weight):
        table[0][weight] = 0
    find_optimal(items, weight, table, len(items)-1)
    print("The optimal value is: {}".format(table[index-2][weight]))

#The core of the algorithm. At every point in the process where we can make a decision
# there are two options. We can take the current item, in which case the total
# value will be that item plus the set of optimal choices we can make now that the
# weight of that item is in the knapsack. The other choice is to ignore the item
# and calculate the optimal value of the set of choices going forward with the
# weight and value of the ignored item not added. The algorithm takes the max of
# both of those options and chooses the one that has the higher total value.

#items is the weights with benefits, weight is current available weight, table
#is the memoization table, index is the current item to search
def find_optimal(items, weight, table, index):
    # Base Case
    if index == 0 or weight == 0:
        table[index][weight] = 0

    #Current weight is more than current available weight, ignore item
    elif (items[index+1][0] > weight):
        table[index][weight] = find_optimal(items, weight, table, index-1)
        #Decide if it is better to skip the current item or include it. This is
        #done by finding what value results form both choices in the long run
        #and deciding optimally
    else:
        choose = items[index+1][1] + find_optimal(items, weight - items[index+1][0], table, index-1)
        skip = find_optimal(items, weight, table, index-1)
        table[index][weight] = max(choose, skip)
    return table[index][weight]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("A filename was not specified, exiting.")
        sys.exit()
    if not os.path.isfile(sys.argv[1]):
        print("Could not see the specified file, exiting.")
        sys.exit()
    zero_one_knapsack(sys.argv[1])
