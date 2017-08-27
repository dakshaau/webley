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
`-t`, `--target` | Specify CSV file with target value. Defaults to 'target.csv'
`-d`, `--data` | Specify CSV file with menu data. Defaults to 'data.csv'

The target file should contain data as follows
```
target,$15.05
```
The value `$15.05` can be anything as long as it is specified to a precision of 2 decimal places and begins with '$'.

All menu items should also be specified in the same format in a separate CSV file.