from fastapi import APIRouter, Request


router = APIRouter(prefix='/event')


@router.post('/on_task_update', status_code=200)
async def on_task_update(request: Request):
    async with request.form() as form:
        print(form.items())
