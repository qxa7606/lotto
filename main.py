from datetime import datetime
import glob
import os
from tabulate import tabulate

book_count = {
    '1': 250,
    '2': 250,
    '3': 100,
    '5': 100,
    '10': 50,
    '20': 50,
	'30': 50
}

prices_of_games = {
    '1408': 1,
    '1460': 20,
    '1439': 20,
    '1400': 10,
    '1465': 10,
    '1448': 10,
    '1456': 10,
    '1450': 5,
    '1466': 5,
    '1408': 1,
    '1463': 1,
    '1455': 1,
    '1444': 2,
    '1393': 2,
    '1429': 2,
    '1458': 5,
    '1461': 5,
    '1479': 5,
    '1447': 5,
    '1440': 5,
    '1424': 5,
    '1443': 5,
    '1441': 5,
    '1419': 10,
    '1454': 1,
    '1451': 3,
    '1473': 3,
    '1482': 5,
    '1449': 10,
    '1425': 20,
    '1395': 5,
    '1471': 1,
    '1423': 2,
	'1470': 2,
	'1472': 10,
	'1468': 30,
	'1405': 5,
	'1431': 5,
	'1407': 5,
	'1442': 3
}

# add 1 for actual num
special_endings = {
    29: 77,
    30: 44,
	0: 6
}


def copy_data():
    with open("data.txt", 'r') as stream:
        data = stream.read().splitlines()
        data = [int(x) for x in data]

    now = datetime.now()
    dt = now.strftime("%Y-%m-%d_%H%M%S") + '.txt'

    with open(f'temp/{dt}', 'w+') as stream:
        for x in data:
            stream.write(f'{x}\n')


def get_data_and_prices():
    list_of_files = sorted(
        filter(lambda x: '-' in x, glob.glob('temp/*.txt')), reverse=True)
    new = list_of_files[0]
    old = list_of_files[1]
    with open(new, 'r') as stream:
        new_data = stream.read().splitlines()
        new_data = [int(x) for x in new_data]
    with open(old, 'r') as stream:
        old_data = stream.read().splitlines()
        old_data = [int(x) for x in old_data]
    return new_data, old_data


def getNum(s):
    if (s == '0' or s == 0):
        return 0
    return int(str(s)[11:14])


def getPrice(s):
    if (s == '0' or s == 0):
        return 0
    return prices_of_games[str(s)[0:4]]


def getGame(s):
    if (s == '0' or s == 0):
        return 0
    return str(s)[0:4]


def get_sales(new_data, old_data, num_slots):
    sales = []
    for i in range(num_slots):
        sale = 0
        # end of book
        if (getNum(new_data[i]) == 0):
            if (getNum(old_data[i]) != 0):
                pc = getPrice(old_data[i])
                if i in special_endings:
                    sale = (getNum(old_data[i]) - special_endings[i]) * pc
                    print('REMOVE index ' + str(i) + 'from special endings')
                else:
                    sale = getNum(old_data[i]) * pc
        # something still in the slot
        else:
            # previous was 0
            if (getNum(old_data[i]) == 0):
                sale = (book_count[str(getPrice(new_data[i]))] -
                        getNum(new_data[i])) * getPrice(new_data[i])
            # previous was non-0
            else:
                # normal decrease
                if (getNum(new_data[i]) <= getNum(old_data[i])) and (getGame(new_data[i]) == getGame(old_data[i])):
                    sale = (
                        getNum(old_data[i]) - getNum(new_data[i])) * getPrice(new_data[i])
                # new book
                else:
                    old_sale = getNum(old_data[i]) * getPrice(old_data[i])
                    if i in special_endings:
                        old_sale = (
                            getNum(old_data[i]) - special_endings[i]) * getPrice(old_data[i])
                        print('REMOVE index ' + str(i) + 'from special endings')
                    new_sale = (book_count[str(getPrice(new_data[i]))] -
                                getNum(new_data[i])) * getPrice(new_data[i])
                    sale = old_sale + new_sale
        sales.append(sale)
    return sales


def main():
    copy_data()
    new, old = get_data_and_prices()
    num_slots = max(len(new), len(old))
    sales = get_sales(new, old, num_slots)
    # print(sales)
    print(f'Total Sales: {sum(sales)}')

    print(
        tabulate(
            [
                ['Old'] + [str(x)[11:14] for x in old],
                ['New'] + [str(x)[11:14] for x in new],
                ['Sales'] + sales
            ],
            ['Slot'] + [x + 1 for x in range(num_slots + 1)]
        )
    )

    print(f'Total Sales: {sum(sales)}')


main()
