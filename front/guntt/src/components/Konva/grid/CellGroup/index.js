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
const react_1 = __importStar(require("react"));
const luxon_1 = require("luxon");
const _konva_1 = require("../../@konva");
const TimelineContext_1 = require("../../timeline/TimelineContext");
const theme_1 = require("../../utils/theme");
const time_resolution_1 = require("../../utils/time-resolution");
const GridCellGroup = ({ column, index, dayInfo, hourInfo }) => {
    const { columnWidth, resolution: { sizeInUnits, unit, unitAbove }, rowHeight, theme: { color: themeColor }, dateLocale, workTime } = (0, TimelineContext_1.useTimelineContext)();
    const cellLabel = (0, react_1.useMemo)(() => (0, time_resolution_1.displayAboveInterval)(column, unitAbove, dateLocale), [column, unitAbove, dateLocale]);
    const points = (0, react_1.useMemo)(() => [0, 0, 0, rowHeight], [rowHeight]);
    // WorkTime logic
    const daysInInterval = (0, react_1.useMemo)(() => {
        let count = 0;
        for (const interval of workTime.intervals) {
            if (column.intersection(interval)) {
                count += 1;
            }
        }
        return count;
    }, [index]);
    const daysBeforeIntevalEnd = (0, react_1.useMemo)(() => {
        let count = 0;
        for (const interval of workTime.intervals) {
            if (!(interval.isBefore(column.end))) {
                return count;
            }
            count += 1;
        }
        return count;
    }, [index]);
    // end of this shit
    const unitAboveInUnitBelow = (0, react_1.useMemo)(() => {
        switch (unitAbove) {
            case 'day':
                return 9 / sizeInUnits;
            case 'week':
                return luxon_1.Duration.fromObject({ [unitAbove]: 1 }).as(unit) / sizeInUnits / ((24 * 7) / (9 * daysInInterval));
            case 'month':
                return luxon_1.Duration.fromObject({ ["day"]: dayInfo.thisMonth }).as("week") / sizeInUnits;
            default:
                return luxon_1.Duration.fromObject({ [unitAbove]: 1 }).as(unit) / sizeInUnits;
        }
    }, [sizeInUnits, dayInfo, unitAbove, unit, index]);
    const unitAboveSpanInPx = (0, react_1.useMemo)(() => {
        return unitAboveInUnitBelow * columnWidth;
    }, [columnWidth, unitAboveInUnitBelow]);
    const xPos = (0, react_1.useMemo)(() => {
        if (unitAbove === "month") {
            const pxUntil = dayInfo.untilNow !== dayInfo.thisMonth
                ? luxon_1.Duration.fromObject({ ["day"]: dayInfo.untilNow - dayInfo.thisMonth }).as("week") / sizeInUnits
                : 0;
            if (hourInfo.backHour) {
                const hourInMonthPx = columnWidth / 168;
                return pxUntil * columnWidth + unitAboveSpanInPx + hourInMonthPx;
            }
            if (hourInfo.nextHour) {
                const hourInMonthPx = columnWidth / 168;
                return pxUntil * columnWidth + unitAboveSpanInPx - hourInMonthPx;
            }
            return pxUntil * columnWidth + unitAboveSpanInPx;
        }
        if (unitAbove === "day") {
            if (hourInfo.backHour) {
                return index * unitAboveSpanInPx + columnWidth / sizeInUnits;
            }
            if (hourInfo.nextHour) {
                return index * unitAboveSpanInPx - columnWidth / sizeInUnits;
            }
        }
        if (unitAbove === "week") {
            if (hourInfo.backHour) {
                return index * unitAboveSpanInPx + columnWidth / 24;
            }
            if (hourInfo.nextHour) {
                return index * unitAboveSpanInPx - columnWidth / 24;
            }
        }
        // let res = index * unitAboveSpanInPx
        switch (unitAbove) {
            case 'day':
                return unitAboveSpanInPx * daysInInterval * daysBeforeIntevalEnd;
            case 'week':
            default:
                return unitAboveSpanInPx / daysInInterval * daysBeforeIntevalEnd;
        }
    }, [index, unitAboveSpanInPx, columnWidth, sizeInUnits, dayInfo, unitAbove, hourInfo]);
    const yPos = (0, react_1.useMemo)(() => rowHeight * 0.3, [rowHeight]);
    const xPosLabel = (0, react_1.useMemo)(() => {
        if (unitAbove === "month") {
            return xPos - unitAboveSpanInPx;
        }
        if (unitAbove === "day") {
            if (hourInfo.backHour) {
                return index * unitAboveSpanInPx + columnWidth / sizeInUnits;
            }
            if (hourInfo.nextHour) {
                return index * unitAboveSpanInPx - columnWidth / sizeInUnits;
            }
        }
        const res = (unitAboveSpanInPx / daysInInterval * daysBeforeIntevalEnd) - unitAboveSpanInPx;
        return res;
    }, [xPos, unitAboveSpanInPx, unitAbove, index, columnWidth, sizeInUnits, hourInfo]);
    const stroke = (0, react_1.useMemo)(() => {
        if (themeColor === "black") {
            return theme_1.DEFAULT_STROKE_LIGHT_MODE;
        }
        return theme_1.DEFAULT_STROKE_DARK_MODE;
    }, [themeColor]);
    return (react_1.default.createElement(_konva_1.KonvaGroup, { key: `timeslot-${index}` },
        react_1.default.createElement(_konva_1.KonvaLine, { x: xPos, y: 0, points: points, stroke: stroke, strokeWidth: 1 }),
        react_1.default.createElement(_konva_1.KonvaText, { align: "center", fill: themeColor, x: xPosLabel, y: yPos - 8, text: xPosLabel !== Infinity ? cellLabel : '', width: unitAboveSpanInPx })));
};
exports.default = GridCellGroup;
