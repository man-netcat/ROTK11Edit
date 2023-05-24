class bidict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reverse_dict = {v: k for k, v in self.items()}

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.reverse_dict[value] = key

    def __delitem__(self, key):
        value = self[key]
        super().__delitem__(key)
        del self.reverse_dict[value]

    def getr(self, value):
        """Return the key corresponding to the given value"""
        return self.reverse_dict.get(value)

    def __hash__(self):
        return hash(frozenset(self.items()))
