from src.bitrix.requests import (
    get_department_info,
    get_staff_from_department_id,
    get_work_schedule,
    get_staff_tasks,
)
from src.bitrix.utils.date_range import generate_date_range
from src.bitrix.websocket_schemas import DepartmentSchema, ResultSchema, StaffSchema, TaskSchema


async def fetch_task_data():
    """Валидирует данные"""

    staff_lst = []  # для передачи в get_staff_tasks
    staff_dict = {}  # для валидации через pydantic

    departments_data = await get_department_info()
    departments = {item["ID"]: item for item in departments_data}

    for dep in departments:
        staff_data = await get_staff_from_department_id(dep)
        staff_lst.extend(staff_data)

        for item in staff_data:
            staff_dict[item["ID"]] = item

    tasks_data = await get_staff_tasks(staff_lst)
    tasks = {i["id"]: i for t in tasks_data if t for i in t}

    work_days = await get_work_schedule()
    date_data = generate_date_range(start, end, work_days)

    result = ResultSchema(
        departments={k: DepartmentSchema(**v) for k, v in departments.items()},
        staff={k: StaffSchema(**v) for k, v in staff_dict.items()},
        tasks={k: TaskSchema(**v) for k, v in tasks.items()},
        interval=date_data,
    )

    return result
