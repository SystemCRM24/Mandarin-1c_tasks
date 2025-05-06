"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importStar(require("react"));
const react_konva_1 = require("react-konva");
const luxon_1 = require("luxon");
const TimelineContext_1 = require("../../../timeline/TimelineContext");
const line_1 = require("../../utils/line");
const tasks_1 = require("../../utils/tasks");
const Line_1 = __importDefault(require("../Line"));
const TaskLine_1 = __importDefault(require("../TaskLine"));
const Tooltip_1 = __importDefault(require("../Tooltip"));
/**
 * This component renders a set of tasks as a Konva Layer.
 * Tasks are displayed accordingly to their assigned resource (different vertical / row position) and their timing (different horizontal / column position)
 * `TasksLayer` is also responsible of handling callback for task components offering base implementation for click, leave and over.
 *
 * The playground has a canvas that simulates 1 day of data with 1 hour resolution.
 * Depending on your screen size you might be able to test also the horizontal scrolling behaviour.
 */
const LayerLine = ({ setTaskTooltip, taskTooltip, create, onTaskEvent }) => {
    const { columnWidth, drawRange, interval, resolution, resources, rowHeight, tasks, toolTip, validLine, workTime } = (0, TimelineContext_1.useTimelineContext)();
    const [workLine, setWorkLine] = (0, react_1.useState)([""]);
    const { start: intervalStart, end: intervalEnd } = interval;
    const getResourceById = (0, react_1.useCallback)((resourceId) => resources.findIndex(({ id }) => resourceId === id), [resources]);
    const getTaskById = (0, react_1.useCallback)((taskId) => tasks.find(({ id }) => taskId === id), [tasks]);
    const onTaskLeave = (0, react_1.useCallback)(() => setTaskTooltip(null), [setTaskTooltip]);
    const onTaskOver = (0, react_1.useCallback)((taskId, point) => {
        const task = getTaskById(taskId);
        if (!task) {
            return setTaskTooltip(null);
        }
        const { x, y } = point;
        setTaskTooltip({ task, x, y });
    }, [getTaskById, setTaskTooltip]);
    const getXCoordinate = (0, react_1.useCallback)((offset) => (offset * columnWidth) / resolution.sizeInUnits, [columnWidth, resolution.sizeInUnits]);
    const getTaskXCoordinate = (0, react_1.useCallback)((startTime) => {
        const timeStart = luxon_1.DateTime.fromMillis(startTime);
        let startOffsetInUnit = timeStart.diff(intervalStart);
        // WorkTime logic
        const nonWorkTimeDiff = workTime.calcOuterNonWorkDuration(timeStart, 'day');
        startOffsetInUnit = startOffsetInUnit.minus(nonWorkTimeDiff);
        // end
        const res = getXCoordinate(startOffsetInUnit.as(resolution.unit));
        return res;
    }, [getXCoordinate, intervalStart, resolution.unit]);
    const getTaskWidth = (0, react_1.useCallback)(({ start, end }) => {
        const timeStart = luxon_1.DateTime.fromMillis(start);
        const timeEnd = luxon_1.DateTime.fromMillis(end);
        let widthOffset = timeEnd.diff(timeStart);
        // WorkTime logic
        const nonWorkTimeDiff = workTime.calcNonWorkDuration(timeEnd, timeStart);
        widthOffset = nonWorkTimeDiff.isValid ? widthOffset.minus(nonWorkTimeDiff) : widthOffset;
        // end
        const result = widthOffset.as(resolution.unit);
        return getXCoordinate(result);
    }, [getXCoordinate, resolution]);
    if (!intervalStart || !intervalEnd) {
        return null;
    }
    if (drawRange.end - drawRange.start <= 0) {
        return null;
    }
    return (react_1.default.createElement(react_konva_1.Layer, null,
        validLine &&
            validLine.map((data) => {
                const startResourceIndex = getResourceById(data.startResId);
                if (startResourceIndex < 0 || workLine.includes(data.id)) {
                    return null;
                }
                //line
                const yCoordinate = (0, tasks_1.getTaskYCoordinate)(startResourceIndex, rowHeight) + (rowHeight * tasks_1.TASK_HEIGHT_OFFSET) / 2;
                const endResourceIndex = getResourceById(data.endResId);
                const endY = (0, tasks_1.getTaskYCoordinate)(endResourceIndex, rowHeight) + (rowHeight * tasks_1.TASK_HEIGHT_OFFSET) / 2;
                const startLine = getTaskXCoordinate(data.start);
                const endLine = getTaskXCoordinate(data.end);
                return (react_1.default.createElement(Line_1.default, { key: `Layer${data.id}`, points: [
                        startLine,
                        yCoordinate,
                        startLine + line_1.LINE_OFFSET,
                        yCoordinate,
                        endLine - line_1.LINE_OFFSET,
                        endY,
                        endLine,
                        endY,
                    ] }));
            }),
        tasks.map((taskData) => {
            const { resourceId, time } = taskData;
            const resourceIndex = getResourceById(resourceId);
            if (resourceIndex < 0) {
                return null;
            }
            const { color: resourceColor, toCompleteColor } = resources[resourceIndex];
            const xCoordinate = getTaskXCoordinate(time.start);
            const yCoordinate = (0, tasks_1.getTaskYCoordinate)(resourceIndex, rowHeight);
            const width = getTaskWidth(time);
            if (xCoordinate > drawRange.end || xCoordinate + width < drawRange.start) {
                return null;
            }
            return (react_1.default.createElement(TaskLine_1.default, { key: `task-${taskData.id}`, data: taskData, fill: resourceColor, fillToComplete: toCompleteColor, onLeave: onTaskLeave, onOver: onTaskOver, x: xCoordinate, y: yCoordinate, width: width, disabled: create, onTaskEvent: onTaskEvent, workLine: setWorkLine }));
        }),
        toolTip && taskTooltip && react_1.default.createElement(Tooltip_1.default, Object.assign({}, taskTooltip))));
};
exports.default = LayerLine;
