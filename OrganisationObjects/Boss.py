"""
BOSS - object that represents the boss of this entire organisation tree. This would be the root node in the tree.
"""
class Boss:
    # boss object only has these two attributes to be inferred from dataset
    def __init__(self, name, uin):
        self.name = name
        self.uin = uin
