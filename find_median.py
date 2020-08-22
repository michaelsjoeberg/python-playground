# find_median.py

class MedianFinder:

	def __init__(self):
		'''
		init
		'''

		self.lst = []

	def addNum(self, num: int) -> None:
		self.lst.append(num)
		self.lst.sort()

	def findMedian(self) -> float:
		if (len(self.lst) % 2 == 0):
			upper = self.lst[int((len(self.lst) / 2))]
			lower = self.lst[int((len(self.lst) / 2) - 1)]

			return float((upper + lower) / 2)
		
		else:
			return float(self.lst[int((len(self.lst) / 2))])


obj = MedianFinder()

obj.addNum(1)
obj.addNum(1)

print(obj.findMedian())

obj.addNum(2)
obj.addNum(3)
obj.addNum(6)

print(obj.findMedian())