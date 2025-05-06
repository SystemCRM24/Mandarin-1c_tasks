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
Object.defineProperty(exports, "__esModule", { value: true });
exports.useTimelineContext = exports.TimelineProvider = void 0;
const react_1 = __importStar(require("react"));
const luxon_1 = require("luxon");
const resources_1 = require("../resources/utils/resources");
const tasks_1 = require("../tasks/utils/tasks");
const dimensions_1 = require("../utils/dimensions");
const logger_1 = require("../utils/logger");
const time_1 = require("../utils/time");
const time_2 = require("../utils/time");
const time_resolution_1 = require("../utils/time-resolution");
const utils_1 = require("../utils/utils");
const workTime_1 = require("../utils/workTime");
const TimelineContext = (0, react_1.createContext)(undefined);
// TODO#lb: this should be another data type, specific to drawing
const DEFAULT_DRAW_RANGE = { start: 0, end: 0 };
const TimelineProvider = ({ children, columnWidth: externalColumnWidth, debug = false, displayTasksLabel = false, dragResolution: externalDragResolution = "1min", enableDrag = true, enableResize = true, headerLabel, hideResources = false, initialDateTime: externalInitialDateTime, onErrors, onTaskClick, onTaskChange, tasks: externalTasks = [], range: externalRange, resolution: externalResolution = "1hrs", resources: externalResources, rowHeight: externalRowHeight, timezone: externalTimezone, theme: externalTheme = "light", localized = {
    start: "Start",
    end: "End",
    duration: "Duration",
    completed: "Completed",
}, dateLocale = "en", onAreaSelect, toolTip = true, customToolTip, enableTaskPattern = true, enableLines, onResourceClick, summary: externalSummary, showSummary, summaryHeader, customResources, workIntervals, isoNow, }) => {
    // WorkTime logic
    const workTime = (0, react_1.useMemo)(() => new workTime_1.WorkTime(workIntervals), [workIntervals]);
    const zone = { zone: 'Europe/Moscow' };
    const [now, setNow] = (0, react_1.useState)(luxon_1.DateTime.local(zone));
    const [delay, setDelay] = (0, react_1.useState)(0);
    (0, react_1.useEffect)(() => document.addEventListener('visibilitychange', () => !document.hidden && updateNow()), []);
    const updateNow = (0, react_1.useCallback)(() => {
        const currentTime = luxon_1.DateTime.local(zone);
        const currentDelay = (60 - currentTime.second) * 1000 - currentTime.millisecond;
        setDelay(currentDelay);
        setNow(currentTime);
    }, []);
    (0, react_1.useEffect)(() => {
        const timeOut = setTimeout(updateNow, delay);
        return () => clearTimeout(timeOut);
    }, [delay]);
    const timezone = (0, react_1.useMemo)(() => {
        if (!externalTimezone) {
            return "system";
        }
        const dateCheck = luxon_1.DateTime.fromMillis(0, { zone: externalTimezone });
        if (!dateCheck.isValid) {
            return "system";
        }
        return externalTimezone;
    }, [externalTimezone]);
    const [drawRange, setDrawRange] = (0, react_1.useState)(DEFAULT_DRAW_RANGE);
    // useEffect(
    //   () => console.log(drawRange),
    //   [drawRange]
    // );
    (0, react_1.useEffect)(() => {
        (0, logger_1.logWarn)("TimelineProvider", `Debug ${debug ? "ON" : "OFF"}`);
        window.__MELFORE_KONVA_TIMELINE_DEBUG__ = debug;
    }, [debug]);
    const range = (0, react_1.useMemo)(() => {
        const { start: externalStart, end: externalEnd } = externalRange;
        const isStart = (0, time_1.isValidRangeTime)(externalStart, "StartRenge");
        const isEnd = (0, time_1.isValidRangeTime)(externalEnd, "EndRange");
        const start = (0, time_1.getValidRangeTime)(externalStart, timezone);
        const end = (0, time_1.getValidRangeTime)(externalEnd, timezone);
        if (isStart) {
            if (start <= end) {
                return { start, end };
            }
            return { start: start, end: start };
        }
        if (isEnd) {
            return { start: end, end: end };
        }
        const now = luxon_1.DateTime.local().toMillis();
        return { start: now, end: now };
    }, [externalRange, timezone]);
    const resolution = (0, react_1.useMemo)(() => (0, utils_1.executeWithPerfomanceCheck)("TimelineProvider", "resolution", () => (0, time_resolution_1.getResolutionData)(externalResolution)), [externalResolution]);
    const interval = (0, react_1.useMemo)(() => (0, utils_1.executeWithPerfomanceCheck)("TimelineProvider", "interval", () => (0, time_2.getIntervalFromInternalTimeRange)(range, resolution, timezone)), [range, resolution, timezone]);
    const TIME_BLOCKS_PRELOAD = (0, react_1.useMemo)(() => {
        const { unit, sizeInUnits } = resolution;
        let timeBlocksPreload = 0;
        switch (unit) {
            case "minute":
                timeBlocksPreload = 60 / sizeInUnits;
                break;
            case "hour":
                timeBlocksPreload = 24 / sizeInUnits;
                break;
            case "day":
                timeBlocksPreload = 7 / sizeInUnits;
                break;
            case "week":
                timeBlocksPreload = 5 / sizeInUnits;
                break;
        }
        return timeBlocksPreload;
    }, [resolution]);
    const initialDateTime = (0, react_1.useMemo)(() => {
        let initial = luxon_1.DateTime.now().toMillis();
        if (externalInitialDateTime) {
            initial = (0, time_1.getValidTime)(externalInitialDateTime, timezone);
            if (Number.isNaN(initial)) {
                initial = new Date().getTime();
            }
        }
        if (initial < range.start || initial > range.end) {
            return range.start;
        }
        return initial;
    }, [externalInitialDateTime, range, timezone]);
    const validTasks = (0, react_1.useMemo)(() => (0, utils_1.executeWithPerfomanceCheck)("TimelineProvider", "validateTasks", () => (0, tasks_1.validateTasks)(externalTasks, range, timezone)), [externalTasks, range, timezone]);
    // Временные блоки которые учавствуют в отображении.
    const timeBlocks = (0, react_1.useMemo)(() => (0, utils_1.executeWithPerfomanceCheck)("TimelineProvider", "timeBlocks", () => interval.splitBy({ [resolution.unit]: resolution.sizeInUnits })
        .filter((interval) => {
        for (const workInterval of workTime.intervals) {
            if (workInterval.intersection(interval)) {
                return true;
            }
        }
        return false;
    })), [interval, resolution]);
    const aboveTimeBlocks = (0, react_1.useMemo)(() => {
        const { unitAbove } = resolution;
        const blocks = [];
        const intervalStart = interval.start;
        const intervalEnd = interval.end;
        let blockStart = intervalStart;
        while (blockStart < intervalEnd) {
            let blockEnd = blockStart.endOf(unitAbove);
            if (blockEnd > intervalEnd) {
                blockEnd = intervalEnd;
            }
            blocks.push(luxon_1.Interval.fromDateTimes(blockStart, blockEnd));
            blockStart = blockEnd.startOf(unitAbove).plus({ [unitAbove]: 1 });
        }
        return blocks;
    }, [interval, resolution]);
    const columnWidth = (0, react_1.useMemo)(() => {
        (0, logger_1.logDebug)("TimelineProvider", "Calculating columnWidth...");
        return !externalColumnWidth || externalColumnWidth < dimensions_1.DEFAULT_GRID_COLUMN_WIDTH
            ? resolution.columnSize
            : externalColumnWidth;
    }, [externalColumnWidth, resolution]);
    const timeblocksOffset = (0, react_1.useMemo)(() => {
        return Math.floor(drawRange.start / columnWidth);
    }, [drawRange, columnWidth]);
    // Отображаемые блоки. Сделано для оптимизации. 
    // правая граница (endIndex) убрана из среза.
    const visibleTimeBlocks = (0, react_1.useMemo)(() => {
        const rangeLength = drawRange.end - drawRange.start;
        if (rangeLength <= 0) {
            return [];
        }
        // if (startIndex > TIME_BLOCKS_PRELOAD) {
        //   startIndex = timeblocksOffset - TIME_BLOCKS_PRELOAD;
        // }
        // const startIndex = timeblocksOffset;
        let endIndex = Math.ceil(drawRange.end / columnWidth);
        if (endIndex < timeBlocks.length - TIME_BLOCKS_PRELOAD) {
            endIndex = endIndex + TIME_BLOCKS_PRELOAD;
        }
        // const endIndex = Math.ceil(drawRange.end / columnWidth);
        const toAdd = Math.ceil(workIntervals.length / 2) + 1;
        // console.log(endIndex, toAdd);
        const vtbs = [...timeBlocks].slice(timeblocksOffset, endIndex + toAdd);
        // const vtbs = [...timeBlocks];
        return vtbs;
    }, [timeblocksOffset, columnWidth, drawRange, timeBlocks, TIME_BLOCKS_PRELOAD]);
    const visibleRange = (0, react_1.useMemo)(() => {
        let range = null;
        if (visibleTimeBlocks && visibleTimeBlocks.length) {
            range = {
                start: visibleTimeBlocks[0].start.toMillis() - (4 * 86400000),
                end: visibleTimeBlocks[visibleTimeBlocks.length - 1].end.toMillis(),
            };
        }
        return range;
    }, [visibleTimeBlocks]);
    const tasks = (0, react_1.useMemo)(() => (0, utils_1.executeWithPerfomanceCheck)("TimelineProvider", "filterTasks", () => (0, tasks_1.filterTasks)(validTasks.items, visibleRange)), [validTasks, visibleRange]);
    /*const lineTasks = useMemo(
      () => onLine && LineFilter(validTasks.items, visibleRange),
      [validTasks, visibleRange, onLine]
    );*/
    const allValidTasks = (0, react_1.useMemo)(() => validTasks.items, [validTasks]);
    const validLine = (0, react_1.useMemo)(() => {
        const arrLine = [];
        const startInMillis = (0, time_1.getXCoordinateFromTime)(drawRange.start, resolution, columnWidth, interval);
        const endInMillis = (0, time_1.getXCoordinateFromTime)(drawRange.end, resolution, columnWidth, interval);
        allValidTasks.forEach((item) => {
            if (item.relatedTasks) {
                item.relatedTasks.forEach((kLine) => {
                    const lineEndId = allValidTasks.find((i) => kLine === i.id);
                    if (lineEndId) {
                        if (startInMillis > lineEndId.time.start && startInMillis > item.time.end) {
                            return;
                        }
                        if (endInMillis < item.time.end && endInMillis < lineEndId.time.start) {
                            return;
                        }
                        arrLine.push({
                            id: item.id + lineEndId.id,
                            startId: item.id,
                            endId: lineEndId.id,
                            startResId: item.resourceId,
                            endResId: lineEndId.resourceId,
                            start: item.time.end,
                            end: lineEndId.time.start,
                        });
                    }
                });
            }
        });
        return arrLine;
    }, [allValidTasks, drawRange, columnWidth, resolution, interval]);
    const dragResolution = (0, react_1.useMemo)(() => {
        (0, logger_1.logDebug)("TimelineProvider", "Calculating drag resolution...");
        const start = luxon_1.DateTime.now().toMillis();
        const resData = (0, time_resolution_1.getResolutionData)(externalDragResolution || externalResolution);
        const end = luxon_1.DateTime.now().toMillis();
        (0, logger_1.logDebug)("TimelineProvider", `Drag resolution calculation took ${end - start} ms`);
        return resData;
    }, [externalDragResolution, externalResolution]);
    const resources = (0, react_1.useMemo)(() => (0, resources_1.addHeaderResource)(externalResources, headerLabel), [externalResources, headerLabel]);
    const rowHeight = (0, react_1.useMemo)(() => {
        (0, logger_1.logDebug)("TimelineProvider", "Calculating rowHeight...");
        const rowHeight = externalRowHeight || dimensions_1.DEFAULT_GRID_ROW_HEIGHT;
        return rowHeight < dimensions_1.MINIMUM_GRID_ROW_HEIGHT ? dimensions_1.MINIMUM_GRID_ROW_HEIGHT : rowHeight;
    }, [externalRowHeight]);
    const resourcesContentHeight = (0, react_1.useMemo)(() => {
        (0, logger_1.logDebug)("TimelineProvider", "Calculating resources content height...");
        return rowHeight * resources.length;
    }, [resources, rowHeight]);
    const theme = (0, react_1.useMemo)(() => {
        return {
            color: externalTheme === "dark" ? "white" : "black",
        };
    }, [externalTheme]);
    const summaryWidth = (0, react_1.useMemo)(() => (columnWidth > 120 ? 120 : columnWidth < 60 ? 60 : columnWidth), [columnWidth]);
    (0, react_1.useEffect)(() => {
        if (onErrors) {
            onErrors(validTasks.errors);
        }
    }, [onErrors, validTasks]);
    const summary = (0, react_1.useMemo)(() => {
        return externalSummary ? [{ id: "0summary", label: "Summary" }, ...externalSummary] : [];
    }, [externalSummary]);
    return (react_1.default.createElement(TimelineContext.Provider, { value: {
            aboveTimeBlocks,
            columnWidth,
            displayTasksLabel,
            dragResolution,
            drawRange,
            enableDrag,
            enableResize,
            hideResources,
            initialDateTime,
            interval,
            onErrors,
            onTaskClick,
            onTaskChange,
            resolution,
            resolutionKey: externalResolution,
            resources,
            workTime,
            now,
            resourcesContentHeight,
            rowHeight,
            setDrawRange,
            tasks,
            theme,
            timeBlocks,
            timezone: timezone || "system",
            visibleTimeBlocks,
            blocksOffset: timeblocksOffset,
            localized: localized,
            dateLocale,
            onAreaSelect,
            toolTip,
            customToolTip,
            enableTaskPattern,
            enableLines,
            validLine,
            allValidTasks,
            externalRangeInMillis: range,
            onResourceClick,
            summary,
            showSummary,
            summaryHeader,
            summaryWidth,
            customResources,
        } }, children));
};
exports.TimelineProvider = TimelineProvider;
const useTimelineContext = () => {
    const context = (0, react_1.useContext)(TimelineContext);
    if (context === undefined) {
        throw new Error("useTimelineContext must be used within a TimelineProvider");
    }
    return context;
};
exports.useTimelineContext = useTimelineContext;
