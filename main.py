from datetime import datetime
import glob
import os

num_slots = 24

book_count = {
    '1': 250,
    '2': 250,
    '3': 100,
    '5': 100,
    '10': 50,
    '20': 50
}

def copy_data():
    with open("data.txt", 'r') as stream:
        data = stream.read().splitlines()
        data = [int(x) for x in data]

    now = datetime.now()
    dt = now.strftime("%d-%m-%Y_%H%M%S") + '.txt'

    with open(dt, 'w+') as stream:
        for x in data:
            stream.write(f'{x}\n')

def get_data_and_prices():
    list_of_files = sorted(filter(lambda x: '-' in x, glob.glob('*.txt')), reverse=True)
    new = list_of_files[0]
    old = list_of_files[1]
    with open(new, 'r') as stream:
        new_data = stream.read().splitlines()
        new_data = [int(x) for x in new_data]
    with open(old, 'r') as stream:
        old_data = stream.read().splitlines()
        old_data = [int(x) for x in old_data]
    with open('prices.txt', 'r') as stream:
        prices = stream.read().splitlines()
        prices = [int(x) for x in prices]
    return new_data, old_data, prices

def get_sales(new_data, old_data, prices):
    price_change = {}
    sales = []
    for i in range(num_slots):
        # end of book
        if (new_data[i] == 0):
            pc = prices[i]
            sale = 0
            if (old_data[i] != 0):
                sale = ((book_count[str(pc)] + 1) - old_data[i]) * pc
            sales.append(sale)
        elif (old_data[i] == 0 and new_data[i] > 0):
            pc = prices[i]
            n_pc = int(input(f'Num {i} new price (default {pc})? ') or pc)
            # change price in prices.txt
            if (pc != n_pc):
                price_change[str(i)] = n_pc
            sale = (new_data[i] - 1) * n_pc
            sales.append(sale)
        # normal increase
        elif (new_data[i] > old_data[i]):
            pc = prices[i]
            sale = (new_data[i] - old_data[i]) * pc
            sales.append(sale)
        # new book added (different price), (same price)
        elif (new_data[i] < old_data[i]):
            pc = prices[i]
            n_pc = int(input(f'Num {i} new price (default {pc})? ') or pc)
            # change price in prices.txt
            if (pc != n_pc):
                price_change[str(i)] = n_pc
            old_sales = ((book_count[str(pc)] + 1) - old_data[i]) * pc
            new_sales = (new_data[i] - 1) * n_pc
            sales.append(old_sales + new_sales)
        else:
            sales.append(0)

    if len(price_change):
        new_prices = []
        for i in range(num_slots):
            new_prices.append(price_change.get(str(i), prices[i]))
        try:
            os.remove('prices_old.txt')
        except OSError:
            pass
        os.rename('prices.txt', 'prices_old.txt')

        print()
        print('Updating prices')
        print(f'Old Prices: {prices}')
        print(f'New Prices: {new_prices}')
        print(price_change)
        print()
        with open('prices.txt', 'w+') as stream:
            for x in new_prices:
                stream.write(f'{x}\n')

    return sales

def main():
    copy_data()
    new, old, prices = get_data_and_prices()
    print(old)
    print(new)
    print(prices)
    sales = get_sales(new, old, prices)
    print(sales)
    print(f'Total Sales: {sum(sales)}')


main()
