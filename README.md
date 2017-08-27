# Webley Coding Puzzle

**By:** Daksh Gupta

**Language:** Python 3.6

### Download

To donwload the source code, simply clone the repository in your system
The instructions to run the code or the tests are below.

You can use the following command to clone this repository:
```shell
git clone https://github.com/dakshaau/webley.git
```

### Testing

Doctests are included in the methods, to ensure that the code is working as expected.

They can be executed using the following command:
```shell
python -m doctest -v find_order.py
```
**NOTE:** The code is written in Python 3 so linux users need to use `python3` rather than `python`.

### Execution

To run the program use the following command on your console:
```shell
python find_order.py [OPTIONS]
```
**NOTE:** The code is written in Python 3 so linux users need to use `python3` rather than `python`.

Available options:

Option | Description
--- | ---
`-h` | Help
`-d`, `--data` | Specify path to CSV file with menu data. Defaults to 'data.csv'
`-max`, `--max-items` | Specify INTEGER value to indicate maximum number of items in the combination. The more number of items, the more time it will take to find a solution. Default value is 15 items.
`-v`, `--verbose` | Show debug outputs such as file format error, target price value, menu data etc.

Here is a sample **_data.csv_** file:
```
Target price, $15.05

mixed fruit,$2.15
french fries,$2.75
side salad,$3.35
hot wings,$3.55
mozzarella sticks,$4.20
sampler plate,$5.80
```
The first line of this file should contain a target price value.

Empty lines in the CSV file are also acceptable.

The price may be put in the following formats:
```
$15.00
$15
15.00
15
```
Any format other than the above is not an acceptable format.