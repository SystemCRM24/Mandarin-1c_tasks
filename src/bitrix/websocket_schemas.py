from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel


class DepartmentSchema(BaseModel):
    ID: str
    NAME: str
    SORT: int
    PARENT: str | None = None
    UF_HEAD: str | None = None


class StaffSchema(BaseModel):
    ID: str
    ACTIVE: bool
    NAME: str
    LAST_NAME: str
    SECOND_NAME: Optional[str] = None
    EMAIL: str
    LAST_LOGIN: Optional[str] = None
    DATE_REGISTER: datetime
    TIME_ZONE: Optional[str] = None
    IS_ONLINE: str
    TIMESTAMP_X: Dict | None = None
    PERSONAL_GENDER: Optional[str] = None
    PERSONAL_WWW: Optional[str] = None
    PERSONAL_BIRTHDAY: Optional[str] = None
    PERSONAL_PHONE: Optional[str] = None
    PERSONAL_FAX: Optional[str] = None
    PERSONAL_MOBILE: Optional[str] = None
    PERSONAL_STREET: Optional[str] = None
    PERSONAL_CITY: Optional[str] = None
    PERSONAL_STATE: Optional[str] = None
    PERSONAL_ZIP: Optional[str] = None
    PERSONAL_COUNTRY: str | None = None
    PERSONAL_MAILBOX: Optional[str] = None
    WORK_PHONE: Optional[str] = None
    WORK_POSITION: Optional[str] = None
    UF_EMPLOYMENT_DATE: Optional[str] = None
    UF_DEPARTMENT: List[int]
    USER_TYPE: str


class TaskSchema(BaseModel):
    id: str
    parentId: Optional[str] = None
    title: str
    description: str
    mark: Optional[str] = None
    priority: str | None = None
    multitask: str | None = None
    notViewed: str | None = None
    replicate: str | None = None
    stageId: str | None = None
    createdBy: str | None = None
    createdDate: datetime | None = None
    responsibleId: str | None = None
    changedBy: str | None = None
    changedDate: datetime | None = None
    statusChangedBy: str | None = None
    closedBy: Optional[str] = None
    closedDate: Optional[datetime] = None
    activityDate: datetime
    dateStart: datetime | None = None
    deadline: datetime | None = None
    startDatePlan: str | None = None
    endDatePlan: str | None = None
    guid: str | None = None
    xmlId: Optional[str] = None
    commentsCount: str | None = None
    serviceCommentsCount: str | None = None
    allowChangeDeadline: str | None = None
    allowTimeTracking: str | None = None
    taskControl: str | None = None
    addInReport: str | None = None
    forkedByTemplateId: Optional[str] = None
    timeEstimate: str | None = None
    timeSpentInLogs: Optional[str] = None
    matchWorkTime: str | None = None
    forumTopicId: str | None = None
    forumId: str | None = None
    siteId: str | None = None
    subordinate: str | None = None
    exchangeModified: Optional[str] = None
    exchangeId: Optional[str] = None
    outlookVersion: str | None = None
    viewedDate: datetime | None = None
    sorting: Optional[str] = None
    durationFact: Optional[str] = None
    isMuted: str | None = None
    isPinned: str | None = None
    isPinnedInGroup: str | None = None
    flowId: Optional[str] = None
    descriptionInBbcode: str | None = None
    status: str | None = None
    statusChangedDate: datetime | None = None
    durationPlan: str | None = None
    durationType: str | None = None
    favorite: str | None = None
    groupId: str | None = None
    auditors: List | None = None
    accomplices: List | None = None
    newCommentsCount: int | None = None
    creator: Dict | None = None
    responsible: Dict | None = None
    accomplicesData: List | None = None
    subStatus: str | None = None


class WorkIntervalSchema(BaseModel):
    start: datetime
    end: datetime


class ResultSchema(BaseModel):
    departments: Dict[str, DepartmentSchema]
    staff: Dict[str, StaffSchema]
    tasks: Dict[str, TaskSchema]
    interval: Dict[str, str] | list[dict]
    workIntervals: List[WorkIntervalSchema] | None = None
