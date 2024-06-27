#!/bin/env python
from datetime import datetime
import glob
import os
# from tabulate import tabulate
import csv

book_count = {
    '1': 250,
    '2': 250,
    '3': 100,
    '5': 100,
    '10': 50,
    '20': 50,
	'30': 50
}

def copy_data():
    with open("data.txt", 'r') as stream:
        data = stream.read().splitlines()
        data = [int(x) for x in data]

    now = datetime.now()
    dt = now.strftime("%Y-%m-%d_%H%M%S") + '.txt'

    with open(f'temp/{dt}', 'w+') as stream:
        for x in data[:-1]:
            stream.write(f'{x}\n')
        stream.write(f'{data[-1]}')

# https://www.nylottery.org/information/scratch-off-tickets
def update_game_prices():
    prices = {}
    with open('gamePrices.txt', mode ='r')as file:
        csvFile = csv.reader(file, delimiter='\t')
        for lines in csvFile:
                prices[int(lines[1])] = int(lines[-1][1:])
    return prices

def get_data_and_prices():
    list_of_files = sorted(
        filter(lambda x: '-' in x, glob.glob('temp/*.txt')), reverse=True)
    new = list_of_files[0]
    old = list_of_files[1]
    with open(new, 'r') as stream:
        new_data = stream.read().splitlines()
    with open(old, 'r') as stream:
        old_data = stream.read().splitlines()
    return new_data, old_data

def calc(oldD, newD, gp):
    count = 0
    o = [x[:12] for x in oldD]
    n = [x[:12] for x in newD]
    # o o --
    # x o
    # x x --
    # o x --
    counter = 0
    for nx in n:
        counter += 1
        if len(nx) < 12 or int(nx[:4]) not in gp:
            pass
        elif nx in o:
            oInfo = None
            nInfo = None
            for e in oldD:
                if e[:12] == nx:
                    oInfo = e
            for e in newD:
                if e[:12] == nx:
                    nInfo = e
            curr = (int(oInfo[11:14]) - int(nInfo[11:14])) * gp[int(nx[:4])]
            print(f'{counter}) {nx[:4]} ${gp[int(nx[:4])]} {oInfo[11:14]} -> {nInfo[11:14]} == {curr}')
            count += curr
        else:
            # new game
            nInfo = None
            for e in newD:
                if e[:12] == nx:
                    nInfo = e
            curr = (book_count[str(gp[int(nInfo[:4])])] - int(nInfo[11:14])) * gp[int(nInfo[:4])]
            print(f'{counter}) {nInfo[:4]} ${gp[int(nInfo[:4])]} {gp[int(nInfo[:4])]} -> {nInfo[11:14]} == {curr}')
            count += curr
    counter = 0
    for ox in o:
        counter += 1
        if int(ox[:4]) in gp and ox not in n and len(ox) > 11:
            oInfo = None
            for e in oldD:
                if e[:12] == ox:
                    oInfo = e
            curr = int(oInfo[11:14]) * gp[int(oInfo[:4])]
            print(f'{counter}) {oInfo[:4]} ${gp[int(oInfo[:4])]} {int(oInfo[11:14])} -> 0 == {curr}')
            count += curr
    return count

def main():
    copy_data()
    gp = update_game_prices()
    newD, oldD = get_data_and_prices()
    cnt = calc(oldD, newD, gp)
    print(cnt)
    # 1558 0315083 023 0481458247	
    # 1558 0315083 024 1712516018

    # new, old = get_data_and_prices()
    # num_slots = max(len(new), len(old))
    # sales = get_sales(new, old, num_slots)
    # # print(sales)
    # print(f'Total Sales: {sum(sales)}')

    # print(
    #     tabulate(
    #         [
    #             ['Old'] + [str(x)[11:14] for x in old],
    #             ['New'] + [str(x)[11:14] for x in new],
    #             ['Sales'] + sales
    #         ],
    #         ['Slot'] + [x + 1 for x in range(num_slots + 1)]
    #     )
    # )

    # print(f'Total Sales: {sum(sales)}')


main()
