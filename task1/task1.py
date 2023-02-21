#!/usr/bin/env python
import sys
import csv
import os

class CoffeeCalculator:
    def __init__(self, args):
        self.filename = args[1]
        self.group = args[2]
        self.groupings = {}
        self.rowCount = 0
        self.printedLines = 0

        self.validateInput(args)

    def validateInput(self, args):
        if os.stat(self.filename).st_size == 0:
            print('File is empty.')
            sys.exit(1)

        if not (3 <= len(args) <= 5):
            print('Incorrect number of arguments.')
            sys.exit(1)

        if len(args) >= 4:
            self.selection = args[3].lower()

            if len(args) == 5:
                self.lineLimit = float(args[4])

        if self.group not in ['origin', 'roaster']:
            print(f'Incorrect argument: {self.group}')
            sys.exit(1)

        if self.selection not in [None, 'row_count', 'row_percentage', 'average']:
            print(f'Incorrect argument: {self.selection}')
            sys.exit(1)

    def calculate(self):
            with open(self.filename, encoding="utf8") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')

                for n, row in enumerate(csv_reader):
                    if n == 0:
                        continue

                    name, roaster, roast, locCountry, origin, usd, rating, reviewDate, review = row

                    grouping_key = origin if self.group == 'origin' else roaster
                    if grouping_key not in self.groupings:
                        self.groupings[grouping_key] = []

                    self.groupings[grouping_key].append((name, roaster, roast, locCountry, usd, rating, reviewDate, review))
                    self.rowCount += 1

    def calculateSelection(self):
        for entry in self.groupings:
            self.groupings[entry].append(len(self.groupings[entry]))

        if self.selection == 'row_percentage':
            for entry in self.groupings:
                self.groupings[entry].append((self.groupings[entry][-1]/self.rowCount) * 100)

        elif self.selection == 'average':
            for entry in self.groupings:
                total = 0
                for det in self.groupings[entry]:
                    if not isinstance(det, int):
                        total += float(det[5])
                self.groupings[entry].append(total/float(self.groupings[entry][-1]))


    def printGroups(self):
        for entry in self.groupings:
            print(f'{entry}: \n')
            for det in self.groupings[entry]:
                if not isinstance(det, int):
                    print(f'{det} \n')

    def printCalculations(self):
        sortedGroups = dict(sorted(self.groupings.items(), key=lambda item: item[1][-1], reverse=True))

        for entry in sortedGroups:
            if self.lineLimit:
                if not self.printedLines >= self.lineLimit:
                    print(f'{entry}: {self.groupings[entry][-1]}\n')
                    self.printedLines += 1
            else:
                print(f'{entry}: {self.groupings[entry][-1]}\n')



calc = CoffeeCalculator(sys.argv)

if __name__ == '__main__':
    calc.calculate()
    calc.calculateSelection()
    # calc.printGroups()
    calc.printCalculations()