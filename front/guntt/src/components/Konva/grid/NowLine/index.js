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
const react_konva_1 = require("react-konva");
const _konva_1 = require("../../@konva");
const TimelineContext_1 = require("../../timeline/TimelineContext");
const NowLine = ({ rowHeight, stageHeight, columnWidth }) => {
    const { interval: { start: intervalStart }, resolution, workTime, now, } = (0, TimelineContext_1.useTimelineContext)();
    const x = (0, react_1.useMemo)(() => {
        let startOffsetInUnit = now.diff(intervalStart);
        // WorkTime logic
        const nonWorkTimeDiff = workTime.calcOuterNonWorkDuration(now, 'day');
        startOffsetInUnit = startOffsetInUnit.minus(nonWorkTimeDiff);
        // end
        const offset = startOffsetInUnit.as(resolution.unit);
        return (offset * columnWidth) / resolution.sizeInUnits;
    }, [now, intervalStart, resolution.unit, columnWidth, resolution.sizeInUnits]);
    const text = (0, react_1.useMemo)(() => { var _a; return (_a = now.toISOTime()) === null || _a === void 0 ? void 0 : _a.slice(0, 5); }, [now]);
    return (react_1.default.createElement(react_konva_1.Layer, null,
        react_1.default.createElement(_konva_1.KonvaLine, { x: x, y: rowHeight * 0.8, points: [0, 0, 0, stageHeight], stroke: "red", strokeWidth: 1, dash: [8, 3] }),
        react_1.default.createElement(_konva_1.KonvaText, { fill: "red", x: x, y: rowHeight * 0.8 - 20, text: text, width: columnWidth })));
};
exports.default = NowLine;
