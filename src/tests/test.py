class Test:
    def __init__(self):
        self.attr = 0

    @classmethod
    async def from_schedule(cls, id: str = '1'):
        obj = cls()
        obj.attr = id
        return obj


t = await Test.from_schedule()