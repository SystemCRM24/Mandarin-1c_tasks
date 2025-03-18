from zoneinfo import ZoneInfo
from datetime import datetime

t = {'РА - Мандарин': {'ID': '22', 'NAME': 'РА - Мандарин', 'SORT': 500, 'UF_HEAD': '1'}, 'Дизайнеры': {'ID': '23', 'NAME': 'Дизайнеры', 'SORT': 500, 'PARENT': '22'}, 'ИТ-отдел': {'ID': '24', 'NAME': 'ИТ-отдел', 'SORT': 500, 'PARENT': '22'}, 'Отдел продаж': {'ID': '25', 'NAME': 'Отдел продаж', 'SORT': 500, 'PARENT': '22', 'UF_HEAD': '18'}, 'Замерщик': {'ID': '26', 'NAME': 'Замерщик', 'SORT': 500, 'PARENT': '25'}, 'Цех': {'ID': '27', 'NAME': 'Цех', 'SORT': 500, 'PARENT': '22', 'UF_HEAD': '6001'}, 'Производство': {'ID': '29', 'NAME': 'Производство', 'SORT': 600, 'PARENT': '22'}, 'Макетчик': {'ID': '30', 'NAME': 'Макетчик', 'SORT': 500, 'PARENT': '29'}, 'Монтажник': {'ID': '34', 'NAME': 'Монтажник', 'SORT': 500, 'PARENT': '29'}, 'Печатник/плотер': {'ID': '32', 'NAME': 'Печатник/плотер', 'SORT': 500, 'PARENT': '29'}, 'Поклейщик': {'ID': '35', 'NAME': 'Поклейщик', 'SORT': 500, 'PARENT': '29'}, 'Сварщик': {'ID': '31', 'NAME': 'Сварщик', 'SORT': 500, 'PARENT': '29'}, 'Фрезеровщик': {'ID': '33', 'NAME': 'Фрезеровщик', 'SORT': 500, 'PARENT': '29'}}





MOSCOW_TZ = ZoneInfo('Europe/Moscow')


now = datetime.now(MOSCOW_TZ)

print(now.date(), str(now.time())[:8])