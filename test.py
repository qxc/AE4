import csv

def processCards(fileName = "charSheet.csv"):
    f = open("cards.txt", "w")
    with open(fileName) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            hand = []
            hand.append(row['Hand1'])
            hand.append(row['Hand2'])
            hand.append(row['Hand3'])
            hand.append(row['Hand4'])
            hand.append(row['Hand5'])
            print('\n')
            print (hand)


        
            
    return
