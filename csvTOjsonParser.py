import csv
import json

from data_types.nodes.CompositeNodes import *
from data_types.trees.ComponentTree import ComponentTree
from data_types.trees.TREEutil import strToClass

def parse(inCSV, outJSON):
    with open(inCSV, 'r') as inputFile:
        csv_reader = csv.DictReader(inputFile)

        # root creation
        firstLine = next(csv_reader)
        firstLine['selfHash'] = int(firstLine['selfHash'])
        firstLine['ID'] = firstLine['numberID']
        del firstLine['numberID']
        firstNode = ProjectNode(**firstLine)

        # tree creation
        tree = ComponentTree(firstNode)

        for line in csv_reader:
            # dict cleaning
            line['selfHash'] = int(line['selfHash'])
            line['parentHash'] = int(line['parentHash'])
            line['ID'] = line['numberID']
            del line['numberID']

            # parent extraction
            parent = tree.searchNode(selfHash = line['parentHash'])

            # node class extraction
            classname = line['type']
            if classname == 'Assembly':
                classname = 'AssemblyNode'
                line['level'] = parent.getLevel() + 2
            elif classname == 'Part':
                classname = 'LeafNode'
            elif classname == 'Hardware':
                prefix = line['ID'][1:4]
                if prefix == 'MEH':
                    classname = 'MechanicalNode'
                elif prefix == 'ELH':
                    classname = 'ElectricalNode'
                elif prefix == 'EMH':
                    classname = 'ElectromechanicalNode'
                elif prefix == 'MMH':
                    classname = 'MeasuredNode'
            elif classname == 'Jig':
                classname = 'JigNode'
            elif classname == 'Placeholder':
                classname = 'PlaceholderNode'
            elif classname == 'Product':
                classname = 'ProductNode'

            # node filling
            node = strToClass(classname)(**line)

            # tree filling
            parent.addChild(node)

        # tree cleaning
        for node in tree.iterPreorder():
            node.delFeatures('selfHash', 'parentHash')
            if node.comment == '-':
                node.comment = None
            if node.link == '' or node.link == '-':
                node.link = None
            if node.packageQuantity == '':
                node.packageQuantity = 1
            if node.seller == '' or node.seller == '-':
                node.seller = None
            node.price = float(node.price)
            node.quantity = int(node.quantity)
            node.packageQuantity = int(node.packageQuantity)

        # json loading
        tree.jsonSave(outJSON)

parse('HardwareArchive.csv', 'HardwareArchive.json')