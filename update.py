class update:
    def __init__(self):
        self.updates = {}
        self.lastid = 0
    
    def add(self, event):
        self.lastid += 1
        self.updates[self.lastid] = event
    
    def print_remove(self):
        ret = self.updates.copy()
        self.updates = {}
        return ret