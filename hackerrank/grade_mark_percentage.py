#!/usr/bin/python

# The first line contains the integer N, the number of students.
# The next N lines contains the name and marks obtained by that student separated by a space.
# The final line contains the name of a particular student previously listed.

# TEST INPUT
# test_input = """3
# Krishna 67 68 69
# Arjun 70 98 63
# Malika 52 56 60
# Malika"""

# test_input = test_input.split("\n")

# student = test_input[-1]

# for line in test_input[1:-1]:
#     if line.startswith(student):
#         grades = line.split(" ", 1)[1].split(" ")
#         total_grade = 0
        
#         # calculate average grade

#         for grade in grades:
#             total_grade = total_grade + float(grade)

#         print(total_grade/len(grades))

if __name__ == '__main__':
    n = int(raw_input())
    student_marks = {}

    for _ in range(n):
        line = raw_input().split()
        name, scores = line[0], line[1:]
        scores = map(float, scores)
        student_marks[name] = scores

    query_name = raw_input()

    total_grade = 0
    for grade in student_marks[query_name]:
        total_grade = total_grade + float(grade)

    print("{:.2f}".format(total_grade/len(student_marks[query_name])))