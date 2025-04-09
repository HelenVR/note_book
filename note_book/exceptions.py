class ContactNotFoundError(Exception):
    def __init__(self, name: str):
        super().__init__(f"Contact with name {name} not found.")
        self.name = name

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name})'


class DuplicateContactError(Exception):
    def __init__(self, name: str):
        super().__init__(f"Contact with name {name} already exists.")
        self.name = name

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name})'