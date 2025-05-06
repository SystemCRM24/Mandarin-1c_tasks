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
const _konva_1 = require("../@konva");
const Layer_1 = __importDefault(require("../grid/Layer"));
const Layer_2 = __importDefault(require("../resources/components/Layer"));
const Summary_1 = __importDefault(require("../resources/components/Summary"));
const resources_1 = require("../resources/utils/resources");
const Layer_3 = __importDefault(require("../tasks/components/Layer"));
const LayerLine_1 = __importDefault(require("../tasks/components/LayerLine"));
const tasks_1 = require("../tasks/utils/tasks");
const logger_1 = require("../utils/logger");
const NowLine_1 = __importDefault(require("../grid/NowLine"));
const TimelineContext_1 = require("./TimelineContext");
const DEFAULT_STAGE_SIZE = { height: 0, width: 0 };
const Timeline = () => {
    const { hideResources, initialDateTime, interval, columnWidth, resourcesContentHeight, resolution, setDrawRange, resources, rowHeight, theme: { color: themeColor }, timeBlocks, drawRange, onAreaSelect, enableLines, externalRangeInMillis, showSummary, summaryWidth, workTime, now } = (0, TimelineContext_1.useTimelineContext)();
    const [scrollbarSize, setScrollbarSize] = (0, react_1.useState)(0);
    const [size, setSize] = (0, react_1.useState)(DEFAULT_STAGE_SIZE);
    const [newTask, setNewTask] = (0, react_1.useState)(false);
    const [isMove, setIsMove] = (0, react_1.useState)(false);
    const [newTaskDimension, setNewTaskDimension] = (0, react_1.useState)({ row: 0, width: 0, x: 0, y: 0 });
    const [startXClick, setStartXClick] = (0, react_1.useState)(0);
    const [existTask, setExistTask] = (0, react_1.useState)(false);
    const stageRef = (0, react_1.useRef)(null);
    const wrapper = (0, react_1.useRef)(null);
    const [taskTooltip, setTaskTooltip] = (0, react_1.useState)(null);
    const onWindowResize = (0, react_1.useCallback)(() => {
        if (!wrapper.current) {
            return;
        }
        (0, logger_1.logDebug)("Timeline", "Resizing window...");
        const { clientHeight: height, clientWidth: width, offsetHeight, offsetWidth } = wrapper.current;
        const scrollbarSize = Math.max(offsetHeight - height, offsetWidth - width);
        setSize({ height, width });
        setScrollbarSize(scrollbarSize);
    }, []);
    const onStageScroll = (0, react_1.useCallback)(() => {
        if (!wrapper.current || !stageRef.current) {
            return;
        }
        (0, logger_1.logDebug)("Timeline", "Scrolling stage...");
        const { scrollLeft } = wrapper.current;
        stageRef.current.container().style.transform = `translate(${scrollLeft}px, 0)`;
        stageRef.current.x(-scrollLeft);
        const start = scrollLeft;
        const end = scrollLeft + size.width;
        setDrawRange({ start, end });
        setTaskTooltip(null);
    }, [setDrawRange, size.width]);
    (0, react_1.useEffect)(() => {
        (0, logger_1.logDebug)("Timeline", "Initial applying of onResize event listener...");
        window.addEventListener("resize", onWindowResize);
        onWindowResize();
        return () => {
            window.removeEventListener("resize", onWindowResize);
        };
    }, [onWindowResize]);
    (0, react_1.useEffect)(() => {
        if (!wrapper.current) {
            return;
        }
        (0, logger_1.logDebug)("Timeline", "Initial applying of onScroll event listener...");
        wrapper.current.addEventListener("scroll", onStageScroll);
        onStageScroll();
    }, [onStageScroll]);
    (0, react_1.useEffect)(() => {
        (0, logger_1.logDebug)("Timeline", "Applying effects of size changes...");
        //DrawLayer space calculate
        onWindowResize();
    }, [hideResources, onWindowResize, showSummary]);
    (0, react_1.useEffect)(() => {
        if (!wrapper.current || !initialDateTime) {
            return;
        }
        const timeStart = luxon_1.DateTime.fromMillis(initialDateTime);
        const startOffsetInUnit = timeStart.diff(interval.start).as(resolution.unit);
        wrapper.current.scrollTo({ left: (startOffsetInUnit * columnWidth) / resolution.sizeInUnits });
    }, [columnWidth, initialDateTime, interval, resolution.sizeInUnits, resolution.unit]);
    const fullTimelineWidth = (0, react_1.useMemo)(() => columnWidth * timeBlocks.length, [columnWidth, timeBlocks]);
    // const stageHeight = useMemo(() => size.height, [size]);
    // TODO#lb: check if ok
    const stageHeight = resourcesContentHeight;
    const stageWidth = (0, react_1.useMemo)(() => scrollbarSize + size.width, [scrollbarSize, size]);
    const timelineCommonStyle = (0, react_1.useMemo)(() => ({
        minHeight: resourcesContentHeight,
    }), [resourcesContentHeight]);
    const summaryLeft = (0, react_1.useMemo)(() => {
        return hideResources ? 0 : resources_1.RESOURCE_HEADER_WIDTH;
    }, [hideResources]);
    const timelineWrapperStyle = (0, react_1.useMemo)(() => (Object.assign(Object.assign({}, timelineCommonStyle), { border: `1px solid ${themeColor}`, display: "flex", position: "relative", width: "100%" })), [themeColor, timelineCommonStyle]);
    const resourcesStageWrapperStyle = (0, react_1.useMemo)(() => (Object.assign(Object.assign({}, timelineCommonStyle), { backgroundColor: "transparent", boxShadow: "4px 4px 32px 1px #0000000f", borderRight: `1px solid ${themeColor}`, left: 0, paddingBottom: scrollbarSize, position: "sticky", top: 0, width: resources_1.RESOURCE_HEADER_WIDTH, zIndex: 1 })), [scrollbarSize, themeColor, timelineCommonStyle]);
    const summaryStageWrapperStyle = (0, react_1.useMemo)(() => (Object.assign(Object.assign({}, timelineCommonStyle), { backgroundColor: "transparent", boxShadow: "4px 4px 32px 1px #0000000f", borderRight: `1px solid ${themeColor}`, left: summaryLeft, paddingBottom: scrollbarSize, position: "sticky", top: 0, width: summaryWidth, zIndex: 1 })), [scrollbarSize, themeColor, timelineCommonStyle, summaryWidth, summaryLeft]);
    const startOffset = (0, react_1.useMemo)(() => {
        if (externalRangeInMillis.start === +interval.start) {
            return false;
        }
        return true;
    }, [externalRangeInMillis, interval]);
    // Расчет координаты для начала сетки координат
    const xOfStart = (0, react_1.useMemo)(() => {
        const timeStart = luxon_1.DateTime.fromMillis(externalRangeInMillis.start);
        const startOffsetInUnit = timeStart.diff(interval.start);
        const res = (startOffsetInUnit.as(resolution.unit) * columnWidth) / resolution.sizeInUnits;
        return res;
    }, [externalRangeInMillis, columnWidth, resolution, interval]);
    // Расчет координат для визуального окончания сетки дат
    const xOfEnd = (0, react_1.useMemo)(() => {
        const timeEnd = luxon_1.DateTime.fromMillis(externalRangeInMillis.end);
        let endOffsetInUnit = timeEnd.diff(interval.start);
        // WorkTime logic
        const nonWorkTime = workTime.calcNonWorkDuration(interval.end, interval.start);
        endOffsetInUnit = endOffsetInUnit.minus(nonWorkTime);
        // Back to main
        const res = (endOffsetInUnit.as(resolution.unit) * columnWidth) / resolution.sizeInUnits;
        return res;
    }, [externalRangeInMillis, columnWidth, resolution, interval]);
    const endOffset = (0, react_1.useMemo)(() => {
        return fullTimelineWidth - xOfEnd;
    }, [fullTimelineWidth, xOfEnd]);
    const marginOffset = (0, react_1.useMemo)(() => {
        return columnWidth * 0.015;
    }, [columnWidth]);
    const gridStageWrapperStyle = (0, react_1.useMemo)(() => (Object.assign(Object.assign({}, timelineCommonStyle), { overflow: "hidden", width: fullTimelineWidth - endOffset + marginOffset })), [fullTimelineWidth, timelineCommonStyle, endOffset, marginOffset]);
    const resourcesOffset = (0, react_1.useMemo)(() => (hideResources ? 0 : resources_1.RESOURCE_HEADER_WIDTH + 1), [hideResources]);
    const summaryOffset = (0, react_1.useMemo)(() => (!showSummary ? 0 : summaryWidth), [showSummary, summaryWidth]);
    const gridWrapperStyle = (0, react_1.useMemo)(() => (Object.assign(Object.assign({}, timelineCommonStyle), { left: resourcesOffset + summaryOffset, overflow: "auto", position: "absolute", top: 0, width: `calc(100% - (${resourcesOffset}px + ${summaryOffset}px))` })), [resourcesOffset, timelineCommonStyle, summaryOffset]);
    const createNewTaskData = (0, react_1.useCallback)(() => {
        const taksRange = (0, tasks_1.onEndTimeRange)(newTaskDimension, resolution, columnWidth, interval);
        return { resourceId: resources[newTaskDimension.row].id, range: taksRange };
    }, [newTaskDimension, columnWidth, resolution, interval, resources]);
    const onMouseDown = (0, react_1.useCallback)((e) => {
        if (!onAreaSelect || existTask) {
            return;
        }
        const stage = e.target.getStage();
        const clickId = e.target._id;
        const stageId = stage._id;
        if (clickId === stageId) {
            const pointerPosition = stage.getPointerPosition();
            const resourceIndex = (0, resources_1.findResourceIndexByCoordinate)(pointerPosition.y, rowHeight, resources);
            const y = (0, tasks_1.getTaskYCoordinate)(resourceIndex, rowHeight);
            setStartXClick(drawRange.start + pointerPosition.x);
            setNewTaskDimension({ row: resourceIndex, width: 1, x: drawRange.start + pointerPosition.x, y: y });
            setNewTask(true);
            setIsMove(true);
        }
    }, [resources, rowHeight, drawRange, onAreaSelect, existTask]);
    const onMouseUp = (0, react_1.useCallback)((e) => {
        if (!onAreaSelect || existTask) {
            return;
        }
        const newTask = createNewTaskData();
        onAreaSelect(newTask);
        const stage = e.target.getStage();
        stage.container().style.cursor = "default";
        setIsMove(false);
        setNewTask(false);
        setNewTaskDimension(Object.assign(Object.assign({}, newTaskDimension), { width: 1 }));
    }, [onAreaSelect, createNewTaskData, newTaskDimension, existTask]);
    const onMouseMove = (0, react_1.useCallback)((e) => {
        if (isMove) {
            const stage = e.target.getStage();
            stage.container().style.cursor = "crosshair";
            const xpos = stage.getPointerPosition().x + drawRange.start;
            const width = xpos - startXClick;
            let controlledX = startXClick;
            const controlledWidth = width < 0 ? -1 * width : width;
            if (width < 0) {
                controlledX = xpos;
            }
            setNewTaskDimension(Object.assign(Object.assign({}, newTaskDimension), { x: controlledX, width: controlledWidth }));
        }
    }, [newTaskDimension, isMove, drawRange, startXClick]);
    const taskHeight = (0, react_1.useMemo)(() => {
        return rowHeight * tasks_1.TASK_HEIGHT_OFFSET;
    }, [rowHeight]);
    const [nowBlockX, setNowBlockX] = (0, react_1.useState)(0);
    (0, react_1.useEffect)(() => {
        let nowInterval = null;
        for (const block of timeBlocks) {
            if (block.contains(now)) {
                nowInterval = block;
                break;
            }
        }
        if (nowInterval === null) {
            nowInterval = interval;
        }
        const today = nowInterval.start.startOf('day');
        let endOffsetInUnit = today.diff(interval.start);
        // WorkTime logic
        const nonWorkTime = workTime.calcNonWorkDuration(today, interval.start);
        endOffsetInUnit = endOffsetInUnit.minus(nonWorkTime);
        // Back to main
        const res = (endOffsetInUnit.as(resolution.unit) * columnWidth) / resolution.sizeInUnits;
        nowBlockX != res && setNowBlockX(res);
    }, [timeBlocks, now, interval, columnWidth, resolution, externalRangeInMillis]);
    return (react_1.default.createElement("div", { style: timelineWrapperStyle },
        !hideResources && (react_1.default.createElement("div", { style: resourcesStageWrapperStyle },
            react_1.default.createElement(react_konva_1.Stage, { height: stageHeight, width: resources_1.RESOURCE_HEADER_WIDTH },
                react_1.default.createElement(Layer_2.default, null)))),
        showSummary && (react_1.default.createElement("div", { style: summaryStageWrapperStyle },
            react_1.default.createElement(react_konva_1.Stage, { height: stageHeight, width: summaryWidth },
                react_1.default.createElement(Summary_1.default, null)))),
        react_1.default.createElement("div", { id: "konva-today", "today-x": nowBlockX, ref: wrapper, style: gridWrapperStyle },
            react_1.default.createElement("div", { style: gridStageWrapperStyle },
                react_1.default.createElement(react_konva_1.Stage, { ref: stageRef, height: stageHeight, width: stageWidth, onMouseDown: onMouseDown, onMouseUp: onMouseUp, onMouseMove: onMouseMove },
                    react_1.default.createElement(Layer_1.default, { height: stageHeight }),
                    !enableLines ? (react_1.default.createElement(Layer_3.default, { taskTooltip: taskTooltip, setTaskTooltip: setTaskTooltip, create: newTask, onTaskEvent: setExistTask })) : (react_1.default.createElement(LayerLine_1.default, { taskTooltip: taskTooltip, setTaskTooltip: setTaskTooltip, create: newTask, onTaskEvent: setExistTask })),
                    startOffset && (react_1.default.createElement(react_konva_1.Layer, null,
                        react_1.default.createElement(_konva_1.KonvaLine, { x: xOfStart, y: rowHeight * 0.8, points: [0, 0, 0, stageHeight], stroke: "red", strokeWidth: 1, dash: [8, 3] }),
                        react_1.default.createElement(_konva_1.KonvaText, { fill: "red", x: xOfStart - 13, y: rowHeight * 0.8 - 20, text: "Start", width: columnWidth }))),
                    newTask && (react_1.default.createElement(react_konva_1.Layer, null,
                        react_1.default.createElement(react_konva_1.Rect, { x: newTaskDimension.x, y: newTaskDimension.y, width: newTaskDimension.width, height: taskHeight, fill: "rgba(0, 70, 255, 0.4)", stroke: "rgba(0, 70, 255, 0.9)", strokeWidth: 1, cornerRadius: tasks_1.TASK_BORDER_RADIUS, dash: [8, 8] }))),
                    react_1.default.createElement(NowLine_1.default, { rowHeight: rowHeight, columnWidth: columnWidth, stageHeight: stageHeight }))))));
};
exports.default = Timeline;
