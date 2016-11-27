#Kyle Dahlin

import sys
import os.path

#Program for finding the longest common subsequence in a set of two words.
#A subsequence in this case is a seqeunce of characters from a string that are
#not necessarily continguous but are in the order they appear in the original
#string. For example a subsequence of the word dynamic is "dami". This algorithm
#takes two words and finds the longest subsequence that is present in both words.

#INPUT FILE: a text file containing two lines, each holding one sequence of
#characters. This Implementation counts spaces as characters but can be easily
#modified to ignore spaces and other special characters.

def subsequence(filename):
    first_word = ""
    second_word = ""
    with open(filename) as f:
        first_word = f.readline().strip()
        second_word = f.readline().strip()

        row_length = len(first_word)+1
        column_length = len(second_word)+1
        #2D list to implement memoization. Each index (i, j) in the table
        #is the length of the subsequence at those indexes in each word.
        memo = [[0]*(column_length) for x in range(row_length)]

        length = lcs(row_length - 1, column_length - 1, first_word, second_word, memo)
        #Uncomment the following two lines if you wish to see the memoization
        #table which the "lcs_from_table" method uses to compute the characters
        #that make up the LCS.
        # for row in memo:
        #     print(row)

        LCS = lcs_from_table(first_word, second_word, row_length-1, column_length-1, memo)
        if LCS == "":
            print("There is no LCS between the two strings.")
        else:
            print(LCS)

#The core implementation of the algorithm. The value at memo[i][j] is the length
#of the lcssubsequence at those two points in each word.
def lcs(i, j, first_word, second_word, memo):

    if memo[i][j] == 0:
        if i == 0 or j == 0:
            memo[i][j] = 0
        elif first_word[i - 1] == second_word[j - 1]:
            memo[i][j] = 1 + lcs(i - 1, j - 1, first_word, second_word, memo)
        else:
            memo[i][j] =  max(lcs(i, j-1, first_word, second_word, memo), lcs(i - 1, j, first_word, second_word, memo))

    return memo[i][j]

#Return the characters that make up the LCS given the memoization table that is
#filled after the lcs function is ran.
def lcs_from_table(first_word, second_word, r_index, c_index, memo):
    output = ""
    if memo[r_index][c_index] == 0:
        return output
    while True:
        #The number above is the same number in which case the index needs to be
        #moved up to that spot and the current letter is not part of the LCS.
        if memo[r_index][c_index - 1] == memo[r_index][c_index]:
            c_index -= 1
            continue
        #The number to the right is the same in which case the index needs
        #to be moved to that spot. The current letter is not a part of the LCS.
        if memo[r_index - 1][c_index] == memo[r_index][c_index]:
            r_index -= 1
            continue
        #Diagonal is a different number which means the the current letter must be
        #added to the LCS. If the diagonal is 0 then we already have the complete
        #LCS in the output
        if memo[r_index -1][c_index - 1] != memo[r_index][c_index]:
            output = second_word[c_index - 1] + output
            if memo[r_index -1][c_index - 1] == 0:
                return output
            r_index -= 1
            c_index -= 1
            continue

    return output

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("A filename was not specified, exiting.")
        sys.exit()
    if not os.path.isfile(sys.argv[1]):
        print("Could not see the specified file, exiting.")
        sys.exit()
    subsequence(sys.argv[1])
