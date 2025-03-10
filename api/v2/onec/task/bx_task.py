from os import environ


TASK_GROUP_ID = environ.get('TASK_GROUP_ID')


class BXTask:
    """Представление для информации для задачи"""

    def __init__(self):
        # Метаинформация по задаче
        self.group_id = TASK_GROUP_ID       # задачи из 1с
        self.allow_time_tracking = 'Y'      # Разрешение на трекинг времени
        # Персонал задачи
        self.assigner_id = None
        self.responsible_id: None
        # Информация самой задачи
        self.title = 'New Task'
        self.description = "Default description"
        # Временные метки
        self.date_start = None
        self.deadline = None
        self.start_date_plan = None
        self.end_date_plan = None
        self.time_estimate = None
        # Прикрепленные файлы
        self.webdav_files = None

    def validate(self):
        """Валидация значений"""
        assert isinstance(self.assigner_id, int), f'Не назначен постановщик для задачи {self.title}'
        assert isinstance(self.responsible_id, int), f'Не назначен исполнитель для задачи {self.title}'
        assert isinstance(self.date_start, int), f'Не указано время начала для задачи {self.title}'
        assert isinstance(self.deadline, int), f'Не указан дедлайн для задачи {self.title}'
        assert isinstance(self.start_date_plan, int), f'Не указана плановая дата начала для задачи {self.title}'
        assert isinstance(self.end_date_plan, int), f'Не указана плановая дата окончания для задачи {self.title}'
        assert isinstance(self.time_estimate, int), f'Не указано затрачиваемое время для задачи {self.title}'
        
    @property
    def request(self) -> dict:
        """Возвращает представление объекта в виде словаря для отправки запроса в бытрыкс"""
        request =  {
            "GROUP_ID": self.group_id,
            "ALLOW_TIME_TRACKING": self.allow_time_tracking,
            "CREATED_BY": self.assigner_id,
            "RESPONSIBLE_ID": self.responsible_id,
            "TITLE": self.title,
            "DESCRIPTION": self.description,
            "DATE_START": self.date_start,
            "DEADLINE": self.deadline,
            "START_DATE_PLAN": self.start_date_plan,
            "END_DATE_PLAN": self.end_date_plan,
            "TIME_ESTIMATE": self.time_estimate 
        }
        if self.webdav_files:
            request['UF_TASK_WEBDAV_FILES'] = self.webdav_files
        return request
