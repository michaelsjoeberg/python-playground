# bubble_sort.py

unsorted_list = [14, 33, 27, 35, 10]
print(unsorted_list)

for i in range(len(unsorted_list)):
	for j in range(len(unsorted_list) - 1):
		if unsorted_list[j] > unsorted_list[j + 1]:
			temp = unsorted_list[j]

			# swap positions
			unsorted_list[j] = unsorted_list[j + 1]
			unsorted_list[j + 1] = temp

print(unsorted_list)