from tree import Tree

def build_tree(self):
    print("start to build the tree")
    starttime = datetime.now()

    self.sourcetree = dict()
    for sourceufid in self.sourcedownstream:
        tree = Tree()
        tree.create_node(sourceufid, sourceufid)
        first = True
        for equipmentufid in self.sourcedownstream[sourceufid]:
            equipment = self.equipmentdict[equipmentufid]
            if first:
                tree.create_node(equipment.name, str(equipment.ufid), parent = str(sourceufid))
                first = False
            else:
                parentufid = self.equipmentdict[equipmentufid].parentufid[sourceufid]
                tree.create_node(equipment.name, str(equipment.ufid), parent = str(parentufid))

        tree.show(str(sourceufid))
        self.sourcetree[sourceufid] = tree
    endtime = datetime.now()
    logger.info(endtime - starttime)
    print("finish building the tree")