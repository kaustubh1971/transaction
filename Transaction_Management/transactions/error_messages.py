
class Message():
    # todo, assign the values meaningfully in slabs of 10s, 20s, 30s,
    CODE_MAP = {
            1 : 'Invalid {}',
            2 : 'Cannot delete transaction , inventory present',
            10 : 'Something went wrong',
            101: 'Read Successful',
            102: 'Create Successful',
            103: 'Deleted Successfully'
    }

    @classmethod
    def code(cls, code):
        return cls.CODE_MAP.get(code, 'Unknown')