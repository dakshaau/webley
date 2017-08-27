import argparse
import re
import sys
import itertools


def match_price_pattern(price):
    """
    This function makes sure that the pattern is in the following format:
        $x.xx
    Examples:
        $15.05
        $1.00
        $12341.12

    >>> match_price_pattern('$.90')
    False
    >>> match_price_pattern('$1.00')
    True
    >>> match_price_pattern('$12.900')
    False
    >>> match_price_pattern('$12')
    False
    >>> match_price_pattern('$15.02')
    True
    >>> import random
    >>> price = '$' + ''.join([str(random.randint(0,10)) for i in range(10)])
    >>> price += '.00'
    >>> match_price_pattern(price)
    True
    >>> match_price_pattern(price[:-3])
    False
    >>> match_price_pattern('$0...012')
    False
    >>> match_price_pattern('1.22')
    False
    >>> match_price_pattern('$0*12')
    False
    """
    pattern = re.compile('\$[0-9]+\.[0-9]{2}')
    return True if pattern.fullmatch(price) else False


def parse_data_file(lines):
    """
    This function parses the list of lines in data file containing the menu
    items and returns a dictionary with price as keys and item names as values.

    >>> parse_data_file(['acb,123', 'amc,asd'])
    {}
    >>> {'abc':1.0,'ans':30.0}==parse_data_file(['abc,$1.00\\n','ans,$30.00\\n'])
    True
    >>> {'abc':1.0,'anc':30.01}==parse_data_file(['abc , $1.00\\n','   anc, $30.01\\n'])
    True
    """
    menu_items = {}
    for line in lines:
        item = None
        price = None
        try:
            line = line.strip()
            item, price = line.split(',')
        except Exception as e:
            print('Invalid format price format, {}, for data file ...'.format(
                price
                ))
            print('\nAccepted format: $xxxx.xx')
            print('Examples: $15.00, $1.00, $0.03')
            print('\nExiting ...')
            return {}
        else:
            item = item.strip()
            price = price.strip()
            if match_price_pattern(price):
                menu_items[item] = float(price[1:])
    return menu_items


def breadth_first_search(target, menu):
    """
    This function performs breadth first graph search on the menu items
    to find a combination of itmes whose price sums up to the target value.

    >>> {'a','c','d'} == breadth_first_search(15, {'a':2,'b':4,'c':6,'d':7})
    True
    >>> {'c'} == breadth_first_search(6, {'a':2,'b':4,'c':6,'d':7})
    True
    >>> frozenset() == breadth_first_search(18, {'a':2,'b':4,'c':6,'d':7})
    True
    """
    visited = set()
    queue = [(frozenset([item]), menu[item]) for item in menu]
    while queue:
        combination, cur_sum = queue.pop(0)
        if combination not in visited:
            visited.add(combination)
            if cur_sum < target:
                for item, price in menu.items():
                    new_combination = combination | frozenset([item])
                    if new_combination not in visited:
                        queue.append((new_combination, cur_sum+price))
            if cur_sum == target:
                return combination
        # print(visited)
    return frozenset()


def find_combination(target, menu):
    """
    This function filters the menu items to only contain items that have
    price less than or equal to the target price and feed it to
    breadth_first_search.

    Returns: A frozenset containing combination of menu items.
             An empty frozenset if no combination is possible.
    """
    filtered_menu = dict([(key, value) for key, value in menu.items() if value <= target])
    return breadth_first_search(target, menu)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t',
        '--target',
        help='''Location of CSV file containing target price.
        Defaults to 'target.csv'.
        ''',
        nargs='?',
        const='target.csv',
        required=True,
        )

    parser.add_argument(
        '-d',
        '--data',
        help='''Location of CSV file containing menu data.
        Defaults to 'data.csv'.
        ''',
        nargs='?',
        const='data.csv',
        required=True,
        )

    args = parser.parse_args()
    target = None
    try:
        target = open(args.target, 'r')
    except FileNotFoundError as e:
        print('Unable to find {} ...'.format(args.target))
    except Exception as e:
        print('Unable to open {} ...'.format(args.target))
        print('Try with administrative priviledges.')

    _, target = target.readline().split(',')
    if match_price_pattern(target.strip()):
        target = float(target[1:])
    else:
        print('Price data, {}, not in accepted format ...'.format(target))
        print('\nAccepted format: $xxxx.xx')
        print('Examples: $15.00, $1.00, $0.03')
        print('\nExiting ...')
        sys.exit()

    # print(target)
    data_file = None
    try:
        data_file = open(args.data, 'r')
    except FileNotFoundError as e:
        print('Unable to find {} ...'.format(args.target))
    except Exception as e:
        print('Unable to open {} ...'.format(args.target))
        print('Try with administrative priviledges.')

    menu = parse_data_file(data_file)
    if not menu:
        sys.exit()

    print('Target price: ${:.2f}'.format(target))
    print('\nMenu:')
    for item in menu:
        print('{}\t${:.2f}'.format(item, menu[item]))
    print()

    combination = find_combination(target, menu)
    if len(combination) == 0:
        print('There is no combination of dishes that is equal to the target price')
    else:
        [print(i) for i in combination]
