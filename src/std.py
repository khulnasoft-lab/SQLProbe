import time
import json
from termcolor import colored
from terminaltables import SingleTable

def stdin(message, params, upper=False, lower=False):
    """Ask for option/input from the user"""
    symbol = colored("[OPT]", "magenta")
    current_time = colored("[{}]".format(time.strftime("%H:%M:%S")), "green")

    option = input("{} {} {}: ".format(symbol, current_time, message))

    if upper:
        option = option.upper()
    elif lower:
        option = option.lower()

    while option not in params:
        option = input("{} {} {}: ".format(symbol, current_time, message))

        if upper:
            option = option.upper()
        elif lower:
            option = option.lower()

    return option

def stdout(message, end="\n"):
    """Print a message for the user in the console"""
    symbol = colored("[MSG]", "yellow")
    current_time = colored("[{}]".format(time.strftime("%H:%M:%S")), "green")
    print("{} {} {}".format(symbol, current_time, message), end=end)

def stderr(message, end="\n"):
    """Print an error for the user in the console"""
    symbol = colored("[ERR]", "red")
    current_time = colored("[{}]".format(time.strftime("%H:%M:%S")), "green")
    print("{} {} {}".format(symbol, current_time, message), end=end)

def showsign(message):
    """Show a vulnerable message"""
    print(colored(message, "magenta"))

def dump(array, filename):
    """Save the given array into a file"""
    with open(filename, 'w') as output:
        for data in array:
            output.write(data + "\n")

def dumpjson(array, filename='wtf.json'):
    """Save the scanned result into a file as JSON"""
    jsondata = {}

    for index, result in enumerate(array):
        jsondata[index] = {
            'url': result[0],
            'db': result[1],
            'server': result[2],
            'lang': result[3]
        }

    with open(filename, 'w') as output:
        output.write(json.dumps(jsondata, indent=4))

def printserverinfo(data):
    """Show vulnerable websites in a table"""
    title = " DOMAINS "
    table_data = [["website", "server", "lang"]] + data
    table = SingleTable(table_data, title)
    print(table.table)

def normalprint(data):
    """Show vulnerable websites in a table"""
    title = " VULNERABLE URLS "
    table_data = [["index", "url", "db"]] + [[index+1, url[0], url[1]] for index, url in enumerate(data)]
    table = SingleTable(table_data, title)
    print(table.table)

def fullprint(data):
    """Show vulnerable websites in a table with server info"""
    title = " VULNERABLE URLS "
    table_data = [["index", "url", "db", "server", "lang"]] + [[index+1, each[0], each[1], each[2][0:30], each[3][0:30]] for index, each in enumerate(data)]
    table = SingleTable(table_data, title)
    print(table.table)
