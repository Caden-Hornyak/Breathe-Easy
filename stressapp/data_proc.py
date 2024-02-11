import csv
from itertools import dropwhile, takewhile

with open(, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    yield next(datareader)

def getstuff(filename):
    with open(filename, "rb") as csvfile:
        datareader = csv.reader(csvfile)

        # yield header
        yield next(datareader)

        for row in datareader:
            if row[3] == criterion:
                yield row
                count += 1
            elif count:
                # done when having read a consecutive series of rows 
                return
            
getstuff(r'C:\Users\19494\Desktop\Coding\Python\StressManWeb\data\netflix_titles.csv')