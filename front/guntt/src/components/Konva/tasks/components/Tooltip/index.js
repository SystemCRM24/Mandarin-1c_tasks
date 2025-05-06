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
const react_konva_utils_1 = require("react-konva-utils");
const luxon_1 = require("luxon");
const TimelineContext_1 = require("../../../timeline/TimelineContext");
const DefaultToolTip_1 = __importDefault(require("./DefaultToolTip"));
const rightMarginOffsetX = -230;
const standardMarginOffsetX = 15;
const marginOffsetY = 25;
const sevenHourinMillis = 25200000;
const twoDayinMillis = 172800000;
/**
 * This component renders a task tooltip inside a canvas.
 */
const TaskTooltip = ({ task, x, y }) => {
    const { drawRange: { end: drawEnd }, resources, localized, customToolTip, workTime } = (0, TimelineContext_1.useTimelineContext)();
    const { label, description, completedPercentage, time: { start, end }, resourceId, } = task;
    const tooltipText = (0, react_1.useMemo)(() => {
        let text = label;
        if (description) {
            text += '\n' + description;
        }
        return text;
    }, [label, description]);
    const startDuration = (0, react_1.useMemo)(() => {
        return luxon_1.DateTime.fromMillis(Number(start)).toFormat("dd/MM/yyyy HH:mm:ss");
    }, [start]);
    const endDuration = (0, react_1.useMemo)(() => {
        return luxon_1.DateTime.fromMillis(Number(end)).toFormat("dd/MM/yyyy HH:mm:ss");
    }, [end]);
    const percentage = (0, react_1.useMemo)(() => {
        return completedPercentage + "%";
    }, [completedPercentage]);
    const duration = (0, react_1.useMemo)(() => {
        // WorkTime logic
        // const part = Number(end) - Number(start);
        const part = workTime.calcWorkDuration(luxon_1.DateTime.fromMillis(Number(end)), luxon_1.DateTime.fromMillis(Number(start))).toMillis();
        if (part < sevenHourinMillis) {
            const min = luxon_1.Duration.fromObject({ ["millisecond"]: part }).as("minute");
            return { time: Math.round(min * 10) / 10, unit: "min" };
        }
        if (part < twoDayinMillis) {
            const hour = luxon_1.Duration.fromObject({ ["millisecond"]: part }).as("hour");
            return { time: Math.round(hour * 10) / 10, unit: "hour" };
        }
        const day = luxon_1.Duration.fromObject({ ["millisecond"]: part }).as("day");
        return { time: Math.round(day * 10) / 10, unit: "Day" };
    }, [start, end]);
    const offsetToolTip = (0, react_1.useMemo)(() => {
        if (resourceId === resources[1].id) {
            if (x > drawEnd + rightMarginOffsetX) {
                return { x: rightMarginOffsetX, y: marginOffsetY };
            }
            return { x: standardMarginOffsetX, y: marginOffsetY };
        }
        if (resourceId === resources[resources.length - 1].id) {
            if (x > drawEnd + rightMarginOffsetX) {
                return { x: rightMarginOffsetX, y: marginOffsetY * 4 };
            }
            return { x: standardMarginOffsetX, y: marginOffsetY * 4 };
        }
        if (x > drawEnd + rightMarginOffsetX) {
            return { x: rightMarginOffsetX, y: marginOffsetY * 2 };
        }
        return { x: standardMarginOffsetX, y: marginOffsetY * 2 };
    }, [drawEnd, resourceId, x, resources]);
    const customToolTipData = (0, react_1.useMemo)(() => {
        return Object.assign(Object.assign({}, task), { start: startDuration, end: endDuration });
    }, [task, startDuration, endDuration]);
    const toolTip = (0, react_1.useMemo)(() => {
        return !customToolTip ? (react_1.default.createElement(DefaultToolTip_1.default, { duration: duration, endDuration: endDuration, startDuration: startDuration, label: tooltipText, localized: localized, percentage: percentage, completedPercentage: completedPercentage })) : (react_1.default.createElement("div", { style: { minWidth: 190, maxWidth: 251, minHeight: 90, maxHeight: 101, overflow: "hidden" } }, customToolTip(customToolTipData)));
    }, [
        completedPercentage,
        duration,
        endDuration,
        label,
        localized,
        startDuration,
        percentage,
        customToolTip,
        customToolTipData,
    ]);
    return (react_1.default.createElement(react_konva_1.Label, { x: x + offsetToolTip.x, y: y - offsetToolTip.y, opacity: 1 },
        react_1.default.createElement(react_konva_utils_1.Html, null, toolTip)));
};
exports.default = TaskTooltip;
