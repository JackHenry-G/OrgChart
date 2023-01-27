"""
UTIL - this file holds utility functions that may be useful, but not vital, to other parts of the code. This is done
in the interest of reducing code, where functions are used repeatedly. These are not necessarily related to any specific
component of the application so they can be separated here.
"""


# Credit to Claudio Sabato at codefather.tech - https://codefather.tech/blog/check-if-python-string-contains-number/#:~:text=A%20simple%20approach%20to%20check,contains%20at%20least%20one%20number.
def contains_number(value):
    # iterate through every character in the string
    # if one is a digit, then return true, which will break the loop and not check the rest of the string
    # i.e. 'A2swer'. The function will recognising there is a number at index 1, and return back true, signalling the
    # string contains a number
    for character in value:
        if character.isdigit():
            return True
    return False


# display question to user and ensure they enter suitable answer
def get_input_from_user(question, suitable_answers):
    # loop ensures the question is asked until a suitable answer is entered
    while True:
        user_input = input(question)
        if user_input.capitalize() not in suitable_answers:
            print("Not an appropriate choice!") # display error message and loop, so question is asked again
        else:
            break # break the loop, meaning the question will no longer be asked, if the answer passes the check
    return user_input


# Python program for implementation of Insertion Sort - https://www.geeksforgeeks.org/insertion-sort/
# insertion sort is faster for smaller number of inputs (n), as quick sort which is commonly regarded as the quickest algorithm has extra overhead form the recursive function calls.
# it is also more stable and requires less memory.
# this fits perfectly for this solution. As teams are usually very small, usually less than 10 people. The algorithm filters each team, rather than the tree as a whole. So the number of inputs into the search is always small
# time complexity of insertion sort
# best case = o(n) - where lists are short like in this project
# wort case = o(n^2)
# average case = o(n^2)
# Function to do insertion sort
def insertion_sort(arr):
    # Iterate over list - starting from 1, which is the scond value in the list. Then gradually moves to end of list.
    for i in range(1, len(arr)):
        key = arr[i]  # gets value in the list

        # compare current element with element to the left. If element two the left is higher, then it is moved up the list
        # then current element eventually is 'inserted' into correct position of that current iteration  of that current iteration
        # E.g. (with numbers for easier understanding) on list of [4,2,3,1]
        # first pass = [2,4,3,1] - 2 is compared first as 'i' is 1 relating to second element of list . Only 4 moves up.
        # second pass = [2,3,4,1] - 3 is compared. 4 moves up again and 3 is placed where 5 was.
        # third pass = [1,2,3,4] - 1 is compared. Everything moves up one and 1 is placed at the bottom.
        j = i - 1
        while j >= 0 and key.data.firstname < arr[j].data.firstname:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
