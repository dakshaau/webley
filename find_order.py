import argparse
import re
import sys


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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t',
        '--target',
        help='Location of CSV file containing target price.',
        nargs='?',
        default='target.csv',
        const='target.csv',
        )

    parser.add_argument(
        '-d',
        '--data',
        help='Location of CSV file containing menu data.',
        nargs='?',
        default='data.csv',
        const='data.csv',
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
    if match_price_pattern(target):
        target = float(target[1:])
    else:
        print('Price data, {}, not in accepted format ...'.format(target))
        print('\nAccepted format: $xxxx.xx')
        print('Examples: $15.00, $1.00, $0.03')
        print('\nExiting ...')
        sys.exit()

    print(target)
