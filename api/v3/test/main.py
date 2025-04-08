import sys
from pathlib import Path


ROOT = Path(__file__).parent.parent.parent.parent
sys.path.append(str(ROOT))


from api.v3.bitrix.task import BXTask

PARAM_BY_ATTR = {
    'id': 'ID',
    'onec_id': 'UF_AUTO_151992241453',
    'status': 'STATUS',
    'group_id': 'GROUP_ID',
    'allow_time_tracking': 'ALLOW_TIME_TRACKING',
    'last_update': 'UF_AUTO_261370983936',
    'assigner_id': 'CREATED_BY',
    'responsible_id': 'RESPONSIBLE_ID',
    'title': 'TITLE',
    'description': 'DESCRIPTION',
    'created_date': 'CREATED_DATE',
    'deadline': 'DEADLINE',
    'start_date_plan': 'START_DATE_PLAN',
    'end_date_plan': 'END_DATE_PLAN',
    'time_estimate': 'TIME_ESTIMATE',
    'webdav_files': 'UF_TASK_WEBDAV_FILES',
}

async def main():
    r = await BXTask.from_bitrix('1')
    print(r)


import asyncio
asyncio.run(main())