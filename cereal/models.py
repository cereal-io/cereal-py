class Enumeration(object):
    def __init__(self, name=None, type_='enum', symbols=None):
        self.name = name
        self.type_ = type_
        if symbols is None:
            self.symbols = []
        else:
            self.symbols = list(symbols)

    def __repr__(self):
        return '<{}:{}>'.format(self.__class__.__name__, self.name)


class Field(object):
    def __init__(self, rule=None, type_=None, name=None, identifier=None):
        self.rule = rule
        self.type_ = type_
        self.name = name
        self.identifier = identifier

    def __repr__(self):
        return '<{}:{}>'.format(self.__class__.__name__, self.name)


class Message(object):
    def __init__(self, name=None, fields=None):
        self.name = name
        if fields is None:
            self.fields = []
        else:
            self.fields = list(fields)

    def __repr__(self):
        return '<{}:{}>'.format(self.__class__.__name__, self.name)
