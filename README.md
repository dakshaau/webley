# Webley Coding Puzzle

**By:** Daksh Gupta

**Language:** Python 3.6

### Testing

Doctests are included in the methods, to ensure that the code is working as expected.

They can be executed using the following command:
```shell
python -m doctest -v find_order.py
```

### Execution

To run the program use the following command on your console:
```shell
python find_order.py [OPTIONS]
```

Available options:

Option | Description
--- | ---
`-h` | Help
`-d`, `--data` | Specify path to CSV file with menu data. Defaults to 'data.csv'

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
Any other format other than the above is not an acceptable format.