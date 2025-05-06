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
exports.TaskDocs = void 0;
const react_1 = __importStar(require("react"));
const react_konva_1 = require("react-konva");
const luxon_1 = require("luxon");
const _konva_1 = require("../../../@konva");
const resources_1 = require("../../../resources/utils/resources");
const TimelineContext_1 = require("../../../timeline/TimelineContext");
const theme_1 = require("../../../utils/theme");
const line_1 = require("../../utils/line");
const tasks_1 = require("../../utils/tasks");
const Line_1 = __importDefault(require("../Line"));
const TaskResizeHandle_1 = __importDefault(require("../TaskResizeHandle"));
const TASK_DEFAULT_FILL = "#000080";
const INVALIDFILL_TASK_DEFAULT_FILL = "rgb(255,0,0)";
const DISABLED_TASK_DEFAULT_FILL = "rgba(96,96,96, 0.8)";
const TASK_DEFAULT_STROKE_WIDTH = 2;
const TASK_DEFAULT_STROKE_FILL = "rgb(0,0,0)";
(0, react_konva_1.useStrictMode)(true);
/**
 * This component renders a simple task as a rectangle inside a canvas.
 * Each task is rendered by `TasksLayer` component, with a loop on each task provided to `KonvaTimeline`.
 * `TasksLayer` is also responsible of handling callback for task components.
 *
 * Supported events (click, leave, over) respond with callbacks of type:
 * <br />
 *  `(taskId: string, point: KonvaPoint) => void`
 *
 * The playground has a simulated canvas with height: 200px and width: 100%
 */
const TaskLine = ({ data, fill = TASK_DEFAULT_FILL, onLeave, onOver, x, y, width, fillToComplete, disabled, onTaskEvent, workLine, }) => {
    const { columnWidth, displayTasksLabel, dragResolution: { sizeInUnits: dragSizeInUnits, unit: dragUnit }, enableDrag, enableResize, interval, onTaskClick, onTaskChange, resolution, resources, rowHeight, drawRange, enableTaskPattern, allValidTasks, enableLines, validLine, externalRangeInMillis, workTime, now } = (0, TimelineContext_1.useTimelineContext)();
    const { id: taskId, completedPercentage } = data;
    const { sizeInUnits, unit } = resolution;
    const [dragging, setDragging] = (0, react_1.useState)(false);
    const [resizing, setResizing] = (0, react_1.useState)(false);
    const [frontLine, setFrontLine] = (0, react_1.useState)(false);
    const [backLine, setBackLine] = (0, react_1.useState)(false);
    const [anchorPointFront, setAnchorPointFront] = (0, react_1.useState)();
    const [anchorPointBack, setAnchorPointBack] = (0, react_1.useState)();
    const connectFrontLine = (0, react_1.useMemo)(() => {
        const result = validLine === null || validLine === void 0 ? void 0 : validLine.filter((i) => i.startId === data.id);
        return result;
    }, [validLine, data]);
    const connectBackLine = (0, react_1.useMemo)(() => {
        const result = validLine === null || validLine === void 0 ? void 0 : validLine.filter((i) => i.endId === data.id);
        return result;
    }, [validLine, data]);
    const opacity = (0, react_1.useMemo)(() => (dragging || resizing ? 0.5 : 1), [dragging, resizing]);
    const deadline = (0, react_1.useMemo)(() => {
        return data.deadline < data.time.end ? data.deadline : data.time.end;
    }, [data]);
    const mainColor = (0, react_1.useMemo)(() => {
        if (disabled) {
            return DISABLED_TASK_DEFAULT_FILL;
        }
        try {
            const taskColor = deadline > now.toMillis() ? fill : '#dc3545';
            const rgb = (0, theme_1.getRGB)(taskColor);
            return ` rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`;
        }
        catch (error) {
            return INVALIDFILL_TASK_DEFAULT_FILL;
        }
    }, [fill, disabled, deadline, now]);
    const mainStroke = (0, react_1.useMemo)(() => {
        if (disabled) {
            return DISABLED_TASK_DEFAULT_FILL;
        }
        return TASK_DEFAULT_STROKE_FILL;
    }, [disabled]);
    const secondaryStroke = (0, react_1.useMemo)(() => {
        return opacity < 1 ? mainStroke : mainColor;
    }, [opacity, mainColor, mainStroke]);
    const initialTaskDimensions = (0, react_1.useMemo)(() => {
        const row = (0, resources_1.findResourceIndexByCoordinate)(y, rowHeight, resources);
        return { row, width, x, y };
    }, [resources, rowHeight, width, x, y]);
    const taskHeight = (0, react_1.useMemo)(() => rowHeight * tasks_1.TASK_HEIGHT_OFFSET, [rowHeight]);
    const [taskDimensions, setTaskDimensions] = (0, react_1.useState)(initialTaskDimensions);
    // Отвечает за финальную точку, куда можно утащить полоску с задачей.
    const finalPoint = (0, react_1.useMemo)(() => {
        const timeStart = luxon_1.DateTime.fromMillis(externalRangeInMillis.end);
        const startOffsetInUnit = timeStart.diff(interval.start).as(resolution.unit);
        return (startOffsetInUnit * columnWidth) / resolution.sizeInUnits;
    }, [externalRangeInMillis, columnWidth, resolution, interval]);
    // Отвечает за начальные ограничения, куда можно утащить полоску с задачей.
    const startPoint = (0, react_1.useMemo)(() => {
        const timeStart = luxon_1.DateTime.fromMillis(externalRangeInMillis.start);
        const startOffsetInUnit = timeStart.diff(interval.start).as(resolution.unit);
        return (startOffsetInUnit * columnWidth) / resolution.sizeInUnits;
    }, [externalRangeInMillis, columnWidth, resolution, interval]);
    (0, react_1.useEffect)(() => {
        const row = (0, resources_1.findResourceIndexByCoordinate)(y, rowHeight, resources);
        setTaskDimensions({ row, width, x, y });
    }, [resources, rowHeight, width, x, y]);
    const dragSnapInPX = (0, react_1.useMemo)(() => {
        const resolutionInSnapUnit = luxon_1.Duration.fromObject({ [unit]: sizeInUnits }).as(dragUnit);
        const dragSnapInResUnit = dragSizeInUnits / resolutionInSnapUnit;
        const dragSnapInPx = dragSnapInResUnit * columnWidth;
        if (!dragSnapInPx || isNaN(dragSnapInPx)) {
            return 1;
        }
        return dragSnapInPx;
    }, [columnWidth, dragUnit, dragSizeInUnits, sizeInUnits, unit]);
    const taskHandlerBorder = (0, react_1.useMemo)(() => {
        if (taskDimensions.x + taskDimensions.width >= finalPoint) {
            return 2;
        }
        return 0;
    }, [taskDimensions, finalPoint]);
    const getDragPoint = (0, react_1.useCallback)((e) => {
        const { target } = e;
        const dragX = target.x();
        const dragY = target.y();
        return { x: dragX, y: dragY };
    }, []);
    const onTaskMouseEvent = (0, react_1.useCallback)((e, callback) => {
        onTaskEvent(true);
        const stage = e.target.getStage();
        if (!stage) {
            return;
        }
        const point = stage.getPointerPosition();
        if (!point) {
            return;
        }
        callback(taskId, Object.assign(Object.assign({}, point), { x: point.x + drawRange.start }));
    }, [taskId, drawRange, onTaskEvent]);
    const onClick = (0, react_1.useCallback)(() => onTaskClick && onTaskClick(data), [data, onTaskClick]);
    const onTaskLeave = (0, react_1.useCallback)((e) => {
        e.cancelBubble = true;
        if (resizing) {
            return;
        }
        const stage = e.target.getStage();
        if (!stage) {
            return;
        }
        if (enableDrag) {
            stage.container().style.cursor = "default";
        }
        onTaskMouseEvent(e, onLeave);
        onTaskEvent(false);
    }, [enableDrag, onLeave, onTaskMouseEvent, resizing, onTaskEvent]);
    const onTaskOver = (0, react_1.useCallback)((e) => {
        if (disabled) {
            return;
        }
        e.cancelBubble = true;
        if (resizing) {
            return;
        }
        const stage = e.target.getStage();
        if (!stage) {
            return;
        }
        if (enableDrag) {
            stage.container().style.cursor = "move";
        }
        onTaskMouseEvent(e, onOver);
    }, [enableDrag, onOver, onTaskMouseEvent, resizing, disabled]);
    const getXCoordinate = (0, react_1.useCallback)((offset) => (offset * columnWidth) / resolution.sizeInUnits, [columnWidth, resolution.sizeInUnits]);
    const getTaskXCoordinate = (0, react_1.useCallback)((startTime) => {
        const timeStart = luxon_1.DateTime.fromMillis(startTime);
        const startOffsetInUnit = timeStart.diff(interval.start).as(resolution.unit);
        return getXCoordinate(startOffsetInUnit);
    }, [getXCoordinate, interval, resolution.unit]);
    const onDragStart = (0, react_1.useCallback)((e) => {
        const { x, y } = getDragPoint(e);
        const dragFinalX = Math.ceil(x / dragSnapInPX) * dragSnapInPX;
        const xCoordinate = dragFinalX < 0 ? 0 : dragFinalX;
        const resourceIndex = (0, resources_1.findResourceIndexByCoordinate)(y, rowHeight, resources);
        const yCoordinate = (0, tasks_1.getTaskYCoordinate)(resourceIndex, rowHeight);
        const point = { x: xCoordinate, y: yCoordinate };
        // ToolTip save
        onLeave(taskId, point);
        setDragging(true);
        const workLineArr = [];
        if (connectFrontLine) {
            setFrontLine(true);
            const lineData = (0, line_1.getLineData)(connectFrontLine, rowHeight, getTaskXCoordinate, tasks_1.getTaskYCoordinate, "front");
            setAnchorPointFront(lineData.anchorArr);
            workLineArr.push(...lineData.workLineArr);
        }
        if (connectBackLine) {
            setBackLine(true);
            const lineData = (0, line_1.getLineData)(connectBackLine, rowHeight, getTaskXCoordinate, tasks_1.getTaskYCoordinate, "back");
            setAnchorPointBack(lineData.anchorArr);
            workLineArr.push(...lineData.workLineArr);
        }
        workLine(workLineArr);
    }, [
        getDragPoint,
        onLeave,
        resources,
        rowHeight,
        taskId,
        dragSnapInPX,
        workLine,
        getTaskXCoordinate,
        connectBackLine,
        connectFrontLine,
    ]);
    const onDragMove = (0, react_1.useCallback)((e) => {
        const { x, y } = getDragPoint(e);
        const dragFinalX = Math.ceil(x / dragSnapInPX) * dragSnapInPX;
        const xCoordinate = dragFinalX < startPoint ? startPoint : dragFinalX;
        const minY = rowHeight + rowHeight * tasks_1.TASK_OFFSET_Y;
        const maxY = rowHeight * (resources.length - 1) + rowHeight * tasks_1.TASK_OFFSET_Y;
        const taskFinalPoint = finalPoint - taskDimensions.width;
        let controlledY = y;
        let controlledX = xCoordinate;
        if (controlledY < minY) {
            controlledY = minY;
        }
        if (controlledY > maxY) {
            controlledY = maxY;
        }
        if (dragFinalX >= taskFinalPoint) {
            controlledX = taskFinalPoint;
        }
        const point = { x: controlledX, y: controlledY };
        // Tooltip save
        // onTaskOver(e);
        setTaskDimensions((dimensions) => (Object.assign(Object.assign({}, dimensions), point)));
    }, [dragSnapInPX, getDragPoint, resources, finalPoint, rowHeight, taskDimensions, startPoint]);
    const onDragEnd = (0, react_1.useCallback)((e) => {
        setDragging(false);
        if (!onTaskChange) {
            return;
        }
        const { x, y } = getDragPoint(e);
        const dragFinalX = Math.ceil(x / dragSnapInPX) * dragSnapInPX;
        const xCoordinate = dragFinalX < 0 ? 0 : dragFinalX;
        const resourceIndex = (0, resources_1.findResourceIndexByCoordinate)(y + taskHeight / 2, rowHeight, resources);
        const yCoordinate = (0, tasks_1.getTaskYCoordinate)(resourceIndex, rowHeight);
        const point = { x: xCoordinate, y: yCoordinate };
        setTaskDimensions((dimensions) => (Object.assign(Object.assign({}, dimensions), point)));
        const { id: resourceId } = (0, resources_1.findResourceByCoordinate)(y, rowHeight, resources);
        let time = (0, tasks_1.onEndTimeRange)(taskDimensions, resolution, columnWidth, interval);
        // WorkTime logic
        let initialTime = (0, tasks_1.onEndTimeRange)(initialTaskDimensions, resolution, columnWidth, interval);
        time = workTime.onTaskDrag(data.time, initialTime, time);
        // end of this shit
        setFrontLine(false);
        setBackLine(false);
        workLine && workLine([]);
        if (data.relatedTasks) {
            const addTime = +time.end - +data.time.end;
            const tasksId = (0, tasks_1.connectedTasks)(data, allValidTasks, addTime, externalRangeInMillis);
            onTaskChange(Object.assign(Object.assign({}, data), { resourceId, time }), { tasksId: tasksId.allKLine, addTime: tasksId.maxAddTime });
            return;
        }
        onTaskChange(Object.assign(Object.assign({}, data), { resourceId, time }));
    }, [
        rowHeight,
        resources,
        onTaskChange,
        data,
        dragSnapInPX,
        getDragPoint,
        taskHeight,
        taskDimensions,
        resolution,
        columnWidth,
        interval,
        workLine,
        allValidTasks,
        externalRangeInMillis,
    ]);
    const textOffsets = (0, react_1.useMemo)(() => taskHeight / 3, [taskHeight]);
    const textSize = (0, react_1.useMemo)(() => taskHeight / 2.5, [taskHeight]);
    const textStroke = (0, react_1.useMemo)(() => {
        try {
            return (0, theme_1.getContrastColor)(fill);
        }
        catch (error) {
            return "rgb(0,0,0)";
        }
    }, [fill]);
    const textWidth = (0, react_1.useMemo)(() => taskDimensions.width - textOffsets * 2, [taskDimensions, textOffsets]);
    const onResizeStart = (0, react_1.useCallback)((e) => {
        onTaskEvent(true);
        e.cancelBubble = true;
        const { x, y } = getDragPoint(e);
        const dragFinalX = Math.ceil(x / dragSnapInPX) * dragSnapInPX;
        const xCoordinate = dragFinalX < 0 ? 0 : dragFinalX;
        const resourceIndex = (0, resources_1.findResourceIndexByCoordinate)(y, rowHeight, resources);
        const yCoordinate = (0, tasks_1.getTaskYCoordinate)(resourceIndex, rowHeight);
        const point = { x: xCoordinate, y: yCoordinate };
        // onLeave(taskId, point);
        setResizing(true);
        if (x > 0) {
            if (connectFrontLine) {
                setFrontLine(true);
                const lineData = (0, line_1.getLineData)(connectFrontLine, rowHeight, getTaskXCoordinate, tasks_1.getTaskYCoordinate, "front");
                setAnchorPointFront(lineData.anchorArr);
                workLine(lineData.workLineArr);
            }
        }
        else {
            if (connectBackLine) {
                setBackLine(true);
                const lineData = (0, line_1.getLineData)(connectBackLine, rowHeight, getTaskXCoordinate, tasks_1.getTaskYCoordinate, "back");
                setAnchorPointBack(lineData.anchorArr);
                workLine(lineData.workLineArr);
            }
        }
    }, [
        dragSnapInPX,
        getDragPoint,
        onLeave,
        resources,
        rowHeight,
        taskId,
        onTaskEvent,
        workLine,
        getTaskXCoordinate,
        connectBackLine,
        connectFrontLine,
    ]);
    const onResizeMove = (0, react_1.useCallback)((e, handler) => {
        e.cancelBubble = true;
        const { x: dragX } = getDragPoint(e);
        setTaskDimensions((taskDimensions) => {
            const { x: taskX, width: taskWidth } = taskDimensions;
            const handlerX = taskX + dragX;
            const taskEndX = taskX + taskWidth;
            switch (handler) {
                case "rx":
                    if (handlerX <= taskX + tasks_1.TASK_BORDER_RADIUS) {
                        return Object.assign(Object.assign({}, taskDimensions), { handler });
                    }
                    if (handlerX >= finalPoint) {
                        return Object.assign(Object.assign({}, taskDimensions), { width: finalPoint - taskX, handler });
                    }
                    return Object.assign(Object.assign({}, taskDimensions), { width: handlerX - taskX, handler });
                case "lx":
                    if (handlerX >= taskEndX - tasks_1.TASK_BORDER_RADIUS) {
                        return Object.assign(Object.assign({}, taskDimensions), { handler });
                    }
                    if (handlerX <= startPoint) {
                        return Object.assign(Object.assign({}, taskDimensions), { handler });
                    }
                    return Object.assign(Object.assign({}, taskDimensions), { x: handlerX, width: taskEndX - handlerX, handler });
            }
        });
    }, [getDragPoint, finalPoint, startPoint]);
    const onResizeEnd = (0, react_1.useCallback)((e) => {
        setBackLine(false);
        setFrontLine(false);
        onTaskEvent(false);
        e.cancelBubble = true;
        setResizing(false);
        if (!onTaskChange) {
            return;
        }
        let time = (0, tasks_1.onEndTimeRange)(taskDimensions, resolution, columnWidth, interval);
        // WorkTime logic
        time = workTime.onTaskResize(data.time, time, taskDimensions.handler);
        // console.log(data, time)
        // data.time = time;
        // end of this shit
        workLine && workLine([]);
        if (enableLines && data.relatedTasks && frontLine) {
            const addTime = +time.end - +data.time.end;
            const tasksId = (0, tasks_1.connectedTasks)(data, allValidTasks, addTime, externalRangeInMillis);
            onTaskChange(Object.assign(Object.assign({}, data), { time }), { tasksId: tasksId.allKLine, addTime: tasksId.maxAddTime });
            return;
        }
        onTaskChange(Object.assign(Object.assign({}, data), { time }));
    }, [
        onTaskChange,
        data,
        taskDimensions,
        resolution,
        columnWidth,
        interval,
        onTaskEvent,
        enableLines,
        allValidTasks,
        workLine,
        frontLine,
        externalRangeInMillis,
    ]);
    const percentage = (0, react_1.useMemo)(() => {
        if (completedPercentage === 0) {
            return 0.1;
        }
        if (completedPercentage) {
            return (taskDimensions.width / 100) * completedPercentage;
        }
        return taskDimensions.width;
    }, [taskDimensions, completedPercentage]);
    const offsetPercentageX = (0, react_1.useMemo)(() => {
        if (percentage < 22) {
            return percentage;
        }
        if (completedPercentage === 100) {
            return 30;
        }
        return 20;
    }, [completedPercentage, percentage]);
    const offsetPercentageY = (0, react_1.useMemo)(() => taskHeight / 4, [taskHeight]);
    const incompleteColor = (0, react_1.useMemo)(() => {
        try {
            if (disabled) {
                return DISABLED_TASK_DEFAULT_FILL;
            }
            if (fillToComplete) {
                const colorToComplete = (0, theme_1.getRGBA)(fillToComplete);
                if (colorToComplete.a) {
                    const rgba = ` rgba(${colorToComplete.r}, ${colorToComplete.g}, ${colorToComplete.b},${colorToComplete.a})`;
                    return rgba;
                }
                const rgb = ` rgb(${colorToComplete.r}, ${colorToComplete.g}, ${colorToComplete.b})`;
                return rgb;
            }
            const opacity = 0.6;
            const rgb = (0, theme_1.getRGB)(fill);
            //const rgba = ` rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${opacity})`;
            //return rgba;
            return (0, theme_1.RGBFromRGBA)(opacity, rgb);
        }
        catch (error) {
            return "rgba(255, 0, 0, 0.6)";
        }
    }, [fill, fillToComplete, disabled]);
    const noPatternColor = (0, react_1.useMemo)(() => {
        if (disabled) {
            return DISABLED_TASK_DEFAULT_FILL;
        }
        if (dragging || resizing) {
            return incompleteColor;
        }
        return enableTaskPattern ? "transparent" : incompleteColor;
    }, [incompleteColor, enableTaskPattern, disabled, dragging, resizing]);
    const isPercentage = (0, react_1.useMemo)(() => {
        if (typeof completedPercentage !== "number") {
            return false;
        }
        if (completedPercentage >= 0 && completedPercentage <= 100) {
            return true;
        }
        return false;
    }, [completedPercentage]);
    const arrGradientColor = (0, react_1.useMemo)(() => {
        const colors = [];
        const length = 300;
        if (dragging || resizing || typeof completedPercentage !== "number" || disabled || !enableTaskPattern) {
            return [];
        }
        const mainColorLineNumber = Number((11 / (taskDimensions.width / 300)).toFixed(0));
        const incompleteColorLineNumber = Number((16 / (taskDimensions.width / 300)).toFixed(0));
        let mainLineColorCount = 0;
        let incompleteLineColorCount = 0;
        let newColor = 0;
        Array(length)
            .fill(0)
            .forEach((_, index) => {
            const gradientNumber = index * 0.0033;
            if (mainLineColorCount < mainColorLineNumber && incompleteLineColorCount === 0) {
                newColor = gradientNumber;
                mainLineColorCount++;
            }
            if (incompleteLineColorCount !== 0) {
                incompleteLineColorCount++;
            }
            if (mainLineColorCount === mainColorLineNumber) {
                incompleteLineColorCount++;
                mainLineColorCount = 0;
            }
            if (incompleteLineColorCount === incompleteColorLineNumber) {
                incompleteLineColorCount = 0;
                mainLineColorCount = 0;
            }
            colors.push(gradientNumber, newColor === gradientNumber ? mainColor : incompleteColor);
        });
        return colors;
    }, [
        mainColor,
        incompleteColor,
        dragging,
        resizing,
        taskDimensions,
        completedPercentage,
        disabled,
        enableTaskPattern,
    ]);
    const finalGradientX = (0, react_1.useMemo)(() => {
        return taskDimensions.width * Math.cos(45);
    }, [taskDimensions]);
    const finalGradientY = (0, react_1.useMemo)(() => {
        return taskDimensions.width * Math.sin(45);
    }, [taskDimensions]);
    return (react_1.default.createElement(react_konva_1.Group, null,
        react_1.default.createElement(react_konva_1.Group, { x: taskDimensions.x, y: taskDimensions.y, draggable: enableDrag, onClick: onClick, onDragEnd: onDragEnd, onDragMove: onDragMove, onDragStart: onDragStart },
            react_1.default.createElement(react_konva_1.Group, null,
                react_1.default.createElement(react_konva_1.Rect, { id: taskId, cornerRadius: tasks_1.TASK_BORDER_RADIUS, fillLinearGradientStartPoint: { x: 0, y: 0 }, fillLinearGradientEndPoint: { x: finalGradientX, y: finalGradientY }, fillLinearGradientColorStops: arrGradientColor, height: taskHeight, opacity: opacity, stroke: secondaryStroke, strokeWidth: TASK_DEFAULT_STROKE_WIDTH, width: taskDimensions.width }),
                react_1.default.createElement(react_konva_1.Rect, { id: taskId, cornerRadius: tasks_1.TASK_BORDER_RADIUS, fillLinearGradientStartPoint: { x: 0, y: 0 }, fillLinearGradientEndPoint: { x: percentage, y: 0 }, fillLinearGradientColorStops: [1, mainColor, 1, noPatternColor], height: taskHeight, onMouseLeave: onTaskLeave, onMouseMove: onTaskOver, onMouseOver: onTaskOver, opacity: opacity, stroke: mainStroke, strokeWidth: 1, width: taskDimensions.width })),
            isPercentage && (react_1.default.createElement(_konva_1.KonvaText, { fill: textStroke, ellipsis: true, fontSize: 10, text: completedPercentage + "%", width: textWidth, wrap: "none", x: 1 + percentage - offsetPercentageX, y: taskHeight - offsetPercentageY })),
            enableResize && (react_1.default.createElement(TaskResizeHandle_1.default, { height: taskHeight, onResizeStart: onResizeStart, onResizeMove: onResizeMove, onResizeEnd: onResizeEnd, opacity: opacity, position: "lx", taskId: taskId, xCoordinate: 0 })),
            enableResize && (react_1.default.createElement(TaskResizeHandle_1.default, { height: taskHeight, onResizeStart: onResizeStart, onResizeMove: onResizeMove, onResizeEnd: onResizeEnd, opacity: opacity, position: "rx", taskId: taskId, xCoordinate: taskDimensions.width - 3 })),
            displayTasksLabel && (react_1.default.createElement(_konva_1.KonvaText, { fill: completedPercentage === 0 ? "black" : textStroke, ellipsis: true, fontSize: textSize, text: data.label, width: textWidth, wrap: "none", x: textOffsets, y: textOffsets - offsetPercentageY })),
            displayTasksLabel && data.description && (react_1.default.createElement(_konva_1.KonvaText, { fill: completedPercentage === 0 ? "black" : textStroke, ellipsis: true, fontSize: textSize, text: data.description, width: textWidth, wrap: "none", x: textOffsets, y: textOffsets + 5 }))),
        react_1.default.createElement(react_konva_1.Group, null,
            backLine && anchorPointBack && (react_1.default.createElement(react_konva_1.Group, null, anchorPointBack.map((i, index) => {
                return (react_1.default.createElement(Line_1.default, { key: "AB" + index, points: [
                        i.x,
                        i.y,
                        i.x + 20,
                        i.y,
                        taskDimensions.x - 20,
                        taskDimensions.y + taskHeight / 2,
                        taskDimensions.x,
                        taskDimensions.y + taskHeight / 2,
                    ] }));
            }))),
            frontLine && anchorPointFront && (react_1.default.createElement(react_konva_1.Group, null, anchorPointFront.map((i, index) => {
                return (react_1.default.createElement(Line_1.default, { key: "AF" + index, points: [
                        taskDimensions.x + taskDimensions.width,
                        taskDimensions.y + taskHeight / 2,
                        taskDimensions.x + taskDimensions.width + line_1.LINE_OFFSET,
                        taskDimensions.y + taskHeight / 2,
                        i.x - line_1.LINE_OFFSET,
                        i.y,
                        i.x,
                        i.y,
                    ] }));
            }))))));
};
exports.TaskDocs = TaskLine;
exports.default = (0, react_1.memo)(TaskLine);
