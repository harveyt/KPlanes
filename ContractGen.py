#!/usr/bin/python3
#
# Parses ContractTable.csv and outputs actual contracts from snippets.
#
# WARNING: Edit this and ContractTable.csv, not the contracts!
#
import sys
import os
import csv
import re

ROOT = os.getenv('ROOT')
DEST = os.getenv('DEST')
DEBUG = True

# --------------------------------------------------------------------------------

def error(fmt, *a):
    sys.stderr.write("ContractGen.py: error: ")
    sys.stderr.write(fmt.format(*a))
    sys.stderr.write("\n")
    sys.exit(1)

def warning(fmt, *a):
    sys.stderr.write("ContractGen.py: warning: ")
    sys.stderr.write(fmt.format(*a))
    sys.stderr.write("\n")

def debug(fmt, *a):
    if not DEBUG:
        return
    sys.stderr.write("DEBUG: ")
    sys.stderr.write(fmt.format(*a))
    sys.stderr.write("\n")

def output(fmt, *a):
    sys.stdout.write(fmt.format(*a))
    sys.stdout.write("\n")
    
# --------------------------------------------------------------------------------

class ContractType:
    def __init__(self, group, counter, name, data):
        self.group = group
        self.counter = counter
        self.name = re.sub(r'[- ]', '', name)
        self.title = name
        self.data = data

    def dump(self):
        output("    Contract: {}-{}", self.counter, self.name)
        
class ContractGroup:
    def __init__(self, table, group_name):
        self.table = table
        self.group_name = group_name
        self.contract_types = []

    def add_type(self, counter, name, data):
        new_type = ContractType(self, counter, name, data)
        self.contract_types.append(new_type)

    def dump(self):
        output("--------------------------------------------------------------------------------")
        output("Group: {}", self.group_name)
        output("")
        for ct in self.contract_types:
            ct.dump()
        output("")            
        
class ContractTable:
    def __init__(self):
        self.contract_groups = {}
        self._read()

    def find_group(self, group_name):
        if group_name in self.contract_groups:
            return self.contract_groups[group_name]
        new_group = ContractGroup(self, group_name)
        self.contract_groups[group_name] = new_group
        return new_group

    def _read(self):
        with open("{}/ContractTable.csv".format(ROOT), newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            skip = True
            for row in reader:
                if skip:
                    skip = False
                    continue
                group_name = row[0]
                counter = row[2]
                name = row[3]
                group = self.find_group(group_name)
                group.add_type(counter, name, row)

    def dump(self):
        for group_name in self.contract_groups.keys():
            group = self.find_group(group_name)
            group.dump()

# --------------------------------------------------------------------------------

table = ContractTable()
table.dump()
