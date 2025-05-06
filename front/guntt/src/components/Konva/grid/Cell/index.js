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
const _konva_1 = require("../../@konva");
const TimelineContext_1 = require("../../timeline/TimelineContext");
const theme_1 = require("../../utils/theme");
const time_resolution_1 = require("../../utils/time-resolution");
const GridCell = ({ column, height, index, hourInfo: visibleDayInfo }) => {
    const { blocksOffset, columnWidth, resolution: { unit: resolutionUnit }, resolution, rowHeight, dateLocale, theme: { color: themeColor }, } = (0, TimelineContext_1.useTimelineContext)();
    const cellLabel = (0, react_1.useMemo)(() => (0, time_resolution_1.displayInterval)(column, resolutionUnit, dateLocale), [column, resolutionUnit, dateLocale]);
    // WorkTime logic
    const shifts = (0, react_1.useMemo)(() => {
        switch (resolution.label) {
            case "1 Hour":
            case "3 Hours":
                return { divider: 1, label: 0 };
            case "1 Day":
                return { divider: 24 / 9, label: 140 };
            case "1 Week":
            default:
                return { divider: 1.25, label: 150 };
        }
    }, [resolution.label]);
    const xPos = (0, react_1.useMemo)(() => {
        if (resolutionUnit === "day") {
            if (visibleDayInfo.backHour) {
                return columnWidth * (index + blocksOffset) + columnWidth / 24;
            }
            if (visibleDayInfo.nextHour) {
                return columnWidth * (index + blocksOffset) - columnWidth / 24;
            }
        }
        if (resolutionUnit === "week") {
            if (visibleDayInfo.backHour) {
                return columnWidth * (index + blocksOffset) + columnWidth / 168;
            }
            if (visibleDayInfo.nextHour) {
                return columnWidth * (index + blocksOffset) - columnWidth / 168;
            }
        }
        const res = columnWidth * (index + blocksOffset) / shifts.divider;
        return res;
    }, [blocksOffset, columnWidth, index, visibleDayInfo, resolutionUnit, resolution]);
    const yPos = (0, react_1.useMemo)(() => rowHeight * 0.8, [rowHeight]);
    const stroke = (0, react_1.useMemo)(() => {
        if (themeColor === "black") {
            return theme_1.DEFAULT_STROKE_LIGHT_MODE;
        }
        return theme_1.DEFAULT_STROKE_DARK_MODE;
    }, [themeColor]);
    return (react_1.default.createElement(_konva_1.KonvaGroup, { key: `timeslot-${index}` },
        react_1.default.createElement(_konva_1.KonvaLine, { x: xPos, y: yPos, points: [0, 0, 0, height], stroke: stroke, strokeWidth: 1 }),
        react_1.default.createElement(_konva_1.KonvaText, { fill: themeColor, x: xPos - shifts.label, y: yPos - 8, text: cellLabel, width: columnWidth, align: "center" })));
};
exports.default = (0, react_1.memo)(GridCell);
