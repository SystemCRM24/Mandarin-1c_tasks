"use strict";
// Отвечает за отображение полосок и текста на ганте.
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
const _konva_1 = require("../../@konva");
const TimelineContext_1 = require("../../timeline/TimelineContext");
const timeBlockArray_1 = require("../../utils/timeBlockArray");
const Cell_1 = __importDefault(require("../Cell"));
const CellGroup_1 = __importDefault(require("../CellGroup"));
const GridCells = ({ height }) => {
    const { interval, aboveTimeBlocks, visibleTimeBlocks, resolution: { unitAbove }, } = (0, TimelineContext_1.useTimelineContext)();
    const tz = (0, react_1.useMemo)(() => interval.start.toISO().slice(-6), [interval]);
    const dayInfo = (0, react_1.useMemo)(() => (0, timeBlockArray_1.getDaysNumberOfMonths)(unitAbove, aboveTimeBlocks, interval), [unitAbove, aboveTimeBlocks, interval]);
    const aboveHourInfo = (0, react_1.useMemo)(() => (0, timeBlockArray_1.getTimeBlocksTzInfo)(aboveTimeBlocks, tz), [tz, aboveTimeBlocks]);
    const visibileHourInfo = (0, react_1.useMemo)(() => (0, timeBlockArray_1.getTimeBlocksTzInfo)(visibleTimeBlocks, tz), [tz, visibleTimeBlocks]);
    const startUnitAbove = (0, react_1.useMemo)(() => (visibleTimeBlocks.length !== 0 ? visibleTimeBlocks[0].start.startOf(unitAbove) : null), [visibleTimeBlocks, unitAbove]);
    const endUnitAbove = (0, react_1.useMemo)(() => visibleTimeBlocks.length !== 0 ? visibleTimeBlocks[visibleTimeBlocks.length - 1].end.endOf(unitAbove) : null, [visibleTimeBlocks, unitAbove]);
    const arrayIndex = (0, react_1.useMemo)(() => {
        if (visibleTimeBlocks) {
            return [];
        }
        return [];
    }, [visibleTimeBlocks]);
    const aboveTimeBlocksVisible = (0, react_1.useMemo)(() => (0, timeBlockArray_1.getAboveTimeBlocksVisible)(visibleTimeBlocks, aboveTimeBlocks, startUnitAbove, endUnitAbove, arrayIndex), [visibleTimeBlocks, aboveTimeBlocks, startUnitAbove, endUnitAbove, arrayIndex]);
    // const predicate = (item: Interval) => {
    //     if ( item.s.c.hour < 9 || item.s.c.hour >= 18) {
    //         return false;
    //     }
    //     return true;
    // }
    return (react_1.default.createElement(_konva_1.KonvaGroup, null,
        aboveTimeBlocksVisible.map((column, index) => {
            // Эта часть отвечает за отображение информации над временными блоками - самая верхняя часть шкалы времени.
            // Т.е. это номер недели, номер дня в календаре, час и тп.
            return (react_1.default.createElement(CellGroup_1.default, { key: `cell-group-${index}`, column: column, index: arrayIndex[index], dayInfo: dayInfo[arrayIndex[index]], hourInfo: aboveHourInfo[arrayIndex[index]] }));
        }),
        visibleTimeBlocks.map((column, index) => {
            return (react_1.default.createElement(Cell_1.default, { key: `cell-${index}`, column: column, height: height, index: index, hourInfo: visibileHourInfo[index] }));
        })));
};
exports.default = (0, react_1.memo)(GridCells);
