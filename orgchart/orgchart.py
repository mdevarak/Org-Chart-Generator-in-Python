#Copyright (c) 2017, Mohan Devarakonda

import argparse
import csv

class OrgTree(object):
    def __init__(self):
        self.orgList = []
        self.name = None
    def get_node_from_tree(self, org_name):
        if (self.name==org_name):
            return self
        else:
            for node in self.orgList:
                tmp_node = node.get_node_from_tree(org_name)
                if (tmp_node != None):
                    return tmp_node
        return None

    def add_node(self, name):
        node = self.get_node_from_tree(name)
        if (node==None):
            node = OrgTree()
            node.name=name
            return node

    def print_tree(self, level):
        #print "======="
        org_name = self.name
        tabs=""
        for x in range(1, level):
            tabs=tabs+"\t"
        print tabs, org_name
        num_of_orgs=len(self.orgList)
        #print "num_of_orgs", num_of_orgs
        if ( num_of_orgs > 0):
            level=level+1
            for node in self.orgList:
                #print "-----"
                #print "Orgs thread:", org_name
                node.print_tree(level)
                #print "Orgs thread:", org_name, "*****"
            return
        else:
            return

print



def get_org_data():
    with open("../data/ownership_data.csv") as ownfile:
        ownreader = csv.reader(ownfile, delimiter='\t')
        sortedOrglist = sorted(ownreader, key=lambda row: row[0], reverse=False)
    root = OrgTree()
    for row in sortedOrglist:
        name=row[0]
        parent_name=row[1]
        orgType=row[2]
        percentBucket=row[3]
        if (root.name==None):
            root.name=name
            parent_node=OrgTree()
            parent_node.name=parent_name
            root.orgList.append(parent_node)
        else:
            node = root.get_node_from_tree(name)
            parent_node = root.get_node_from_tree(parent_name)
            if (node==None):
                node=root.add_node(name)
            if (parent_node==None):
                parent_node=root.add_node(parent_name)
            node.orgList.append(parent_node)

            #print node.name, parent_node.name, orgType, percentBucket

    root.print_tree(1)
    #print root

def main(args):
    print "args :",  args
    get_org_data()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--org_data_file', '-f', help='The file with hierarchical data for the ', required=False)
    args = parser.parse_args()
    main(args)


