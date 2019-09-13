#!/usr/bin/python

# Mr. Anant Asankhya is the manager at the INFINITE hotel. The hotel has an infinite amount of rooms.

# One fine day, a finite number of tourists come to stay at the hotel. 
# The tourists consist of:
# - A Captain.
# - An unknown group of families consisting of K members per group where K != 1.

# The Captain was given a separate room, and the rest were given one room per group.

# Mr. Anant has an unordered list of randomly arranged room entries. The list consists of the room numbers for all of the tourists. The room numbers will appear K times per group except for the Captain's room.

# Mr. Anant needs you to help him find the Captain's room number. 
# The total number of tourists or the total number of groups of families is not known to you. 
# You only know the value of K and the room number list.

from collections import Counter

K = 5
lst_rooms = [1, 2, 3, 6, 5, 4, 4, 2, 5, 3, 6, 1, 6, 5, 3, 2, 4, 1, 2, 5, 1, 4, 3, 6, 8, 4, 3, 1, 5, 6, 2]

def find_captains_room(K, lst_rooms):
    dict = {}

    # DON'T DO THIS
    # for room in lst_rooms:
    #     room = str(room)
    #     if room not in dict.keys():
    #         dict[str(room)] = 1
    #     else:
    #         dict[str(room)] = dict[room] + 1
    # for room, families in dict.items():
    #     if (families == 1):
    #         print (room)

    # DO THIS
    dict = Counter(lst_rooms)
    print (min(dict, key=dict.get))

find_captains_room(K, lst_rooms)

if __name__ == '__main__':
    K = int(raw_input())
    lst_rooms = list(raw_input().split(" "))

    find_captains_room(K, lst_rooms)

