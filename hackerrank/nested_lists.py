#!/usr/bin/python

# Given the names and grades for each student in a Physics class of N students, 
# store them in a nested list and print the name(s) of any student(s) having 
# the second lowest grade.

# If there are multiple students with the same grade, order their names alphabetically 
# and print each name on a new line.

# The first line contains an integer, N, the number of students. 
# The 2N subsequent lines describe each student over 2 lines; 
#   - the first line contains a student's name
#   - and the second line contains their grade.

def print_second_min_score(students):
    lst_temp = []

    # find min score
    min_score = min(students, key=lambda score: score[1])

    # remove all min score
    for student in sorted(students):
        if (student[1] == min_score[1]):
            students.remove(student)

    # find second min score
    min_score = min(students, key=lambda score: score[1])

    for student in sorted(students):
        if (student[1] == min_score[1]):
            lst_temp.append(student[0])
            print(student[0])

# TEST INPUT
# test_input = """Harry
# 37.21
# Berry
# 37.21
# Tina
# 37.2
# Tina2
# 37.2
# Akriti
# 41
# Harsh
# 39"""

# test_input = test_input.split("\n")

# students = []

# for n in range(len(test_input)):
#     if (n % 2 == 0):
#         name = test_input[n]
#         score = float(test_input[n + 1])
#         students.append([name, score])

# print_second_min_score(students)

students = []
for _ in range(int(raw_input())):
    name = raw_input()
    score = float(raw_input())

    students.append([name, score])

print_second_min_score(students)
