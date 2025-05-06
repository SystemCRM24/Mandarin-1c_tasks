"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.connectedTasks = exports.onEndTimeRange = exports.lineFilter = exports.filterTasks = exports.validateTasks = exports.getTaskYCoordinate = exports.TASK_HEIGHT_OFFSET = exports.TASK_BORDER_RADIUS = exports.TASK_OFFSET_Y = void 0;
const luxon_1 = require("luxon");
const time_1 = require("../../utils/time");
exports.TASK_OFFSET_Y = 0.15;
exports.TASK_BORDER_RADIUS = 4;
exports.TASK_HEIGHT_OFFSET = 0.7;
/**
 * Gets task Y coordinate
 * @param rowIndex the row index
 * @param rowHeight the row height
 */
const getTaskYCoordinate = (rowIndex, rowHeight) => rowHeight * rowIndex + rowHeight * exports.TASK_OFFSET_Y;
exports.getTaskYCoordinate = getTaskYCoordinate;
/**
 * Filters valid tasks to be shown in the chart
 * @param tasks list of tasks as passed to the component
 * @param intervals intervals as passed to the component
 */
const validateTasks = (tasks, range, timezone) => {
    const tz = timezone || "system";
    if (!range || !range.start || !range.end) {
        return { items: [], errors: [{ entity: "timeline", level: "warn", message: "Invalid range" }] };
    }
    if (!tasks || !tasks.length) {
        return { items: [], errors: [{ entity: "timeline", level: "warn", message: "No data" }] };
    }
    const errors = [];
    const items = tasks
        .map((task) => (Object.assign(Object.assign({}, task), { time: {
            start: (0, time_1.getValidTime)(task.time.start, tz),
            end: (0, time_1.getValidTime)(task.time.end, tz),
        }, deadline: (0, time_1.getValidTime)(task.deadline, tz) })))
        .filter(({ id: taskId, time: { start: taskStart, end: taskEnd } }) => {
        if (taskStart >= taskEnd) {
            errors.push({ entity: "task", level: "error", message: "Invalid time", refId: taskId });
            return false;
        }
        if (taskStart < range.start || taskEnd > range.end) {
            errors.push({ entity: "task", level: "warn", message: "Outside range", refId: taskId });
            return false;
        }
        return true;
    });
    return { items, errors };
};
exports.validateTasks = validateTasks;
/**
 * Filters valid tasks to be shown in the chart
 * @param tasks list of tasks as passed to the component
 * @param intervals intervals as passed to the component
 */
const filterTasks = (tasks, range) => {
    if (!range || !range.start || !range.end || !tasks || !tasks.length) {
        return [];
    }
    return tasks.filter(({ time: { start: taskStart, end: taskEnd } }) => {
        if (taskStart >= taskEnd) {
            return false;
        }
        if (taskEnd < range.start || taskStart > range.end) {
            return false;
        }
        return true;
    });
};
exports.filterTasks = filterTasks;
const lineFilter = (tasks, range) => {
    if (!range || !range.start || !range.end || !tasks || !tasks.length) {
        return [];
    }
    return tasks.filter(({ relatedTasks: kLine }) => {
        if (kLine) {
            return true;
        }
        return false;
    });
};
exports.lineFilter = lineFilter;
const fromPxToTime = (sizePx, resolution, columnWidth) => {
    return (sizePx * resolution.sizeInUnits) / columnWidth;
};
const onEndTimeRange = (taskDimesion, resolution, columnWidth, interval) => {
    var _a, _b, _c, _d;
    const columnInHrs = resolution.unit === "week" ? (resolution.sizeInUnits === 1 ? 168 : 336) : 24;
    const hrs = 3600000;
    const hrsInPx = columnWidth / columnInHrs;
    const timeOffset = fromPxToTime(taskDimesion.x, resolution, columnWidth);
    const startTaskMillis = interval.start.plus({ [resolution.unit]: timeOffset }).toMillis();
    const startDate = luxon_1.DateTime.fromMillis(startTaskMillis);
    const startOfBeforeDay = luxon_1.DateTime.fromMillis(startTaskMillis - 3600000).startOf("day");
    const startOfBeforeDayTz = startOfBeforeDay.toISO().slice(-5, -3);
    const startOfNextDay = luxon_1.DateTime.fromMillis(startTaskMillis + 3600000)
        .startOf("day")
        .toISO()
        .slice(-5, -3);
    const intervalStartTZ = (_a = interval.start) === null || _a === void 0 ? void 0 : _a.toISO().slice(-5, -3); //Interval start TZ
    const taskStartTZ = (_b = luxon_1.DateTime.fromMillis(startTaskMillis).startOf("day").toISO()) === null || _b === void 0 ? void 0 : _b.slice(-5, -3); //Task start TZ
    const diffTZ = +intervalStartTZ - +taskStartTZ;
    const startOfDay = (_c = startDate.startOf("day").toISO()) === null || _c === void 0 ? void 0 : _c.slice(-5, -3); //Day start TZ
    const nextDay = (_d = startDate.startOf("day").plus({ day: 1 }).toISO()) === null || _d === void 0 ? void 0 : _d.slice(-5, -3); //Next Day TZ
    const diffTZInDay = +nextDay - +startOfDay;
    let gap = 0;
    let hrsSpecialCase = 0;
    if (resolution.unit === "day" || resolution.unit === "week") {
        if (diffTZ === 1) {
            gap = hrsInPx * diffTZ;
            if (+startOfBeforeDayTz - +intervalStartTZ === 0 && +startOfNextDay - +intervalStartTZ !== 0) {
                gap = 0;
                hrsSpecialCase = hrs;
            }
        }
        if (+startOfBeforeDayTz - +intervalStartTZ !== 0 && +startOfNextDay - +intervalStartTZ === 0) {
            const timeOffsett = fromPxToTime(taskDimesion.x - hrsInPx * 23, resolution, columnWidth);
            const startTaskDayBefore = interval
                .start.plus({ [resolution.unit]: timeOffsett })
                .startOf("hour")
                .toMillis();
            if (startOfBeforeDay.toMillis() === startTaskDayBefore) {
                hrsSpecialCase = hrs;
            }
        }
        if (diffTZ === -1) {
            gap = hrsInPx * diffTZ;
            if (diffTZInDay === -1) {
                gap = hrsInPx * diffTZInDay;
            }
            const timeOffsett = fromPxToTime(taskDimesion.x - hrsInPx * 23, resolution, columnWidth);
            const startTaskDayBefore = interval.start.plus({ [resolution.unit]: timeOffsett }).startOf("hour");
            if (startOfBeforeDay.toMillis() === startTaskDayBefore.toMillis()) {
                if (diffTZInDay !== 0) {
                    gap = 0;
                    hrsSpecialCase = -hrs;
                }
            }
            if (startTaskDayBefore.toMillis() + hrs * 23 === startDate.startOf("day").toMillis() &&
                startTaskDayBefore.toISO().slice(-5, -3) === intervalStartTZ) {
                gap = 0;
                hrsSpecialCase = 0;
            }
        }
    }
    const timeOffsetB = fromPxToTime(taskDimesion.x - gap, resolution, columnWidth);
    const start = interval.start.plus({ [resolution.unit]: timeOffsetB }).toMillis() - hrsSpecialCase;
    const end = start +
        luxon_1.Duration.fromObject({
            [resolution.unit]: fromPxToTime(taskDimesion.width, resolution, columnWidth),
        }).toMillis();
    return { start, end };
};
exports.onEndTimeRange = onEndTimeRange;
const connectedTasks = (taskData, allValidTasks, addTime, range) => {
    const { start, end } = range;
    let allKLine = taskData.relatedTasks ? taskData.relatedTasks : [];
    let newKLine = [];
    let noKLine = true;
    let iOffset = 0;
    let maxAddTime = addTime;
    do {
        noKLine = false;
        let pushCount = iOffset === 0 ? allKLine.length - 1 : 0;
        for (let i = 0 + iOffset; i < allKLine.length; i++) {
            const val = allValidTasks.find((item) => item.id === allKLine[i]);
            if (val) {
                if (+val.time.start + addTime < start) {
                    maxAddTime = start - +val.time.start;
                }
                if (+val.time.end + addTime > end) {
                    maxAddTime = end - +val.time.end;
                }
            }
            if (val === null || val === void 0 ? void 0 : val.relatedTasks) {
                val.relatedTasks.map((value) => {
                    if (!allKLine.includes(value) && !newKLine.includes(value)) {
                        newKLine.push(value);
                        pushCount++;
                    }
                });
            }
        }
        if (newKLine[0]) {
            noKLine = true;
        }
        newKLine.unshift(...allKLine);
        allKLine = [];
        allKLine.push(...newKLine);
        newKLine = [];
        iOffset = iOffset + pushCount;
    } while (noKLine);
    return { allKLine, maxAddTime };
};
exports.connectedTasks = connectedTasks;
