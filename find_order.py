import argparse
import re
import sys
import itertools
from collections import Counter, deque


def match_price_pattern(price):
    """
    This function makes sure that the pattern is in the following format:
        $x.xx
        $x
        x.xx
        x

    Examples:
        $15.05
        $1.00
        $12341.12
        15.05
        3.00
        34
        $15

    >>> match_price_pattern('$.90')
    False
    >>> match_price_pattern('$1.00')
    True
    >>> match_price_pattern('$12.900')
    False
    >>> match_price_pattern('$12')
    True
    >>> match_price_pattern('$15.02')
    True
    >>> import random
    >>> price = '$' + ''.join([str(random.randint(0,10)) for i in range(10)])
    >>> price += '.00'
    >>> match_price_pattern(price)
    True
    >>> match_price_pattern(price[:-3])
    True
    >>> match_price_pattern('$0...012')
    False
    >>> match_price_pattern('1.22')
    True
    >>> match_price_pattern('$0*12')
    False
    >>> match_price_pattern('0.003')
    False
    >>> match_price_pattern('15')
    True
    >>> match_price_pattern('15.')
    False
    >>> match_price_pattern('15.0')
    False
    """
    pattern = re.compile('(\$[0-9]+\.[0-9]{2}|[0-9]+\.[0-9]{2}|[0-9]+|\$[0-9]+)')
    return True if pattern.fullmatch(price) else False


def parse_data_file(lines, verbose=True):
    """
    This function parses the list of lines in data file containing the target
    value and menu items.

    Returns: Target price value (float),
             Menu data (dict)

    >>> targ, menu=parse_data_file(['acb,123', 'amc,asd'])
    Invalid format price format, asd, for data file ...
    <BLANKLINE>
    Accepted formats: $xx.xx, xx.xx, xx
    Examples: $15.00, $1.00, $0.03, $15, 1, 0.03, 15.05
    <BLANKLINE>
    Exiting ...
    >>> targ == 0.
    True
    >>> menu == {}
    True
    >>> targ, menu= parse_data_file(['abc,$1.00\\n','ans,$30.00\\n'])
    >>> targ == 1.
    True
    >>> {'ans':30.0} == menu
    True
    >>> targ, menu = parse_data_file(['abc , $1.00\\n','   anc, $30.01\\n'])
    >>> targ == 1.
    True
    >>> {'anc':30.01} == menu
    True
    >>> targ, menu = parse_data_file(['target,15\\n','\\n','abc, 25.01\\n'])
    >>> targ == 15.
    True
    >>> menu == {'abc': 25.01}
    True
    >>> targ, menu = parse_data_file(['target,15\\n','xcv\\n','abc, 25.01\\n'])
    Invalid CSV file ...
    Exiting ...
    >>> targ == 0.
    True
    >>> menu == {}
    True
    """
    menu_items = {}
    target = 0.
    for ind, line in enumerate(lines):
        item = None
        price = None
        try:
            line = line.strip()
            if 1 < line.count(','):
                raise Exception
            elif line and line.count(',') == 0:
                raise Exception
            else:
                item, price = line.split(',')
        except ValueError as e:
            # Ignoring empty lines
            pass
        except Exception as e:
            if verbose:
                print('Invalid CSV file ...')
                print('Exiting ...')
            return 0., {}
        else:
            item = item.strip()
            price = price.strip()
            if match_price_pattern(price):
                if ind == 0:
                    target = float(price[1:] if '$' in price else price)
                else:
                    menu_items[item] = float(price[1:] if '$' in price else price)
            else:
                if verbose:
                    print('Invalid format price format, {}, for data file ...'.format(
                        price
                        ))
                    print('\nAccepted formats: $xx.xx, xx.xx, xx')
                    print('Examples: $15.00, $1.00, $0.03, $15, 1, 0.03, 15.05')
                    print('\nExiting ...')
                return 0., {}
    return target, menu_items


def breadth_first_search(target, menu, max_level=15):
    """
    This function performs breadth first graph search on the menu items
    to find a combination of itmes whose price sums up to the target value.

    The max_level argument should be an integer which sppecifies the maximum
    depth to be searched before declaring no sulution.

    >>> {'c': 1} == breadth_first_search(6, {'a':2,'b':4,'c':6,'d':7})
    True
    >>> from collections import Counter
    >>> Counter() == breadth_first_search(6.02, {'a':2,'b':4,'c':6,'d':7})
    True
    """
    visited = []
    queue = deque([(Counter([item]), menu[item]) for item in menu])
    while queue:
        combination, cur_sum = queue.popleft()
        if sum(combination.values()) <= max_level:
            if combination not in visited:
                visited.append(combination)
                if cur_sum < target:
                    for item, price in menu.items():
                        new_combination = combination + Counter([item])
                        if new_combination not in visited:
                            queue.append((new_combination, cur_sum+price))
                if cur_sum == target:
                    return combination
            # print(visited)
        else:
            break
    return Counter()


def find_combination(target, menu, max_level):
    """
    This function filters the menu items to only contain items that have
    price less than or equal to the target price and feed it to
    breadth_first_search.

    Returns: A Counter containing combination of menu items.
                OR
             An empty Counter if no combination is possible.
    """
    filtered_menu = dict([(key, value) for key, value in menu.items() if value <= target])
    return breadth_first_search(target, menu, max_level=max_level)


class Parser(argparse.ArgumentParser):
    def error(self, message):
        print()
        print(message)
        print()
        self.print_help()
        sys.exit()

if __name__ == '__main__':
    parser = Parser(description='Webley Coding Puzzle, by Daksh Gupta')
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

    parser.add_argument(
        '-v',
        '--verbose',
        help='''Show debug outputs such as file format error,
        target price value, menu data etc.
        ''',
        action='store_true',
        )

    parser.add_argument(
        '-max',
        '--max-level',
        help='''Specify INTEGER value to indicate maximum level to
        go while searching for a combination. The more levels,
        the more time it will take to find a solution.
        Default value is 15.
        ''',
        type=int,
        default=15,
        )

    try:
        args = parser.parse_args()
    except Exception as e:
        parser.print_help()
    verbosity = args.verbose
    max_level = args.max_level
    data_file = None
    try:
        data_file = open(args.data, 'r')
    except FileNotFoundError as e:
        print('Unable to find {} ...'.format(args.target))
    except Exception as e:
        print('Unable to open {} ...'.format(args.target))
        print('Try with administrative priviledges.')

    target, menu = parse_data_file(data_file, verbosity)
    if not menu:
        sys.exit()

    if verbosity:
        print('Target price: ${:.2f}'.format(target))
        print('\nMenu:')
        for item in menu:
            print('${1:.2f}\t{0}'.format(item, menu[item]))
        print()

    combination = find_combination(target, menu, max_level)
    if len(combination) == 0:
        print('There is no combination of dishes that is equal to the target price')
    else:
        [print('{} {}'.format(combination[item], item)) for item in combination]
