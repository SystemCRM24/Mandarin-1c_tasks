"""
Запросы к битриксу
"""
from fast_bitrix24 import BitrixAsync
import aiocache
from typing import Iterable

from api.v2 import constants


BX = BitrixAsync(constants.BITRIX_WEBHOOK)


async def call_batch(requests: Iterable):
    """Посылает батч-запрос"""
    cmd = {i: r for i, r in enumerate(requests)}
    return await BX.call_batch(params={'halt': 0, 'cmd': cmd})
