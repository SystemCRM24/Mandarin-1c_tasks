import asyncio

class Test:

    @classmethod
    async def from_bitrix(cls, id):
        await asyncio.sleep(1)
        task = cls()
        task.attr = id
        return task
    
    def __init__(self):
        self.attr = 1
    

async def main():
    t = await Test.from_bitrix(2)
    print(t.attr)


asyncio.run(main())