class BXTask:
    """Объект для представления задач в битриксе"""

    __slots__ = (
        'id',
        'onec_id',
        'group_id',
        'allow_time_tracking',
        'last_update',
        'title',
        'description',
        'created_date',
        'deadline',
        'start_date_plan',
        'end_date_plan',
        'time_estimate',
        'webdav_files',
        '__updated'
    )

    PARAM_BY_ATTR = {
        'id',
        'onec_id',
        'group_id',
        'allow_time_tracking',
        'last_update',
        'title',
        'description',
        'created_date',
        'deadline',
        'start_date_plan',
        'end_date_plan',
        'time_estimate',
        'webdav_files',
    }
    
    def __init__(self, ):
        # Идешники задачи
        self.id = None          # Из битры
        self.onec_id = None     # Из 1c
        # Метаинформация по задаче
        self.group_id = None
        self.allow_time_tracking = None
        self.last_update = None
        # Текстовая информация задачи
        self.title = None
        self.description = None
        # Временные метки
        self.created_date = None
        self.deadline = None
        self.start_date_plan = None
        self.end_date_plan = None
        self.time_estimate = None   # Время в секундах
        # Прикрепленные файлы
        self.webdav_files = None
        # Множество для отслеживания изменения атрибутов
        self.__updated = set()
