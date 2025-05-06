"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getAboveTimeBlocksVisible = exports.getDaysNumberOfMonths = exports.getTimeBlocksTzInfo = void 0;
const time_resolution_1 = require("./time-resolution");
const getTimeBlocksTzInfo = (timeBlock, initialTz) => {
    const dayInfoArray = [];
    timeBlock.forEach((column) => {
        var _a;
        const tzStart = (_a = column.start.toISO()) === null || _a === void 0 ? void 0 : _a.slice(-6);
        if (initialTz !== tzStart) {
            if (Number(initialTz === null || initialTz === void 0 ? void 0 : initialTz.slice(1, 3)) - Number(tzStart.slice(1, 3)) > 0) {
                dayInfoArray.push({
                    backHour: true,
                    nextHour: false,
                });
                return;
            }
            if (Number(initialTz === null || initialTz === void 0 ? void 0 : initialTz.slice(1, 3)) - Number(tzStart.slice(1, 3)) < 0) {
                dayInfoArray.push({
                    backHour: false,
                    nextHour: true,
                });
                return;
            }
        }
        dayInfoArray.push({
            backHour: false,
            nextHour: false,
        });
        return;
    });
    return dayInfoArray;
};
exports.getTimeBlocksTzInfo = getTimeBlocksTzInfo;
const getDaysNumberOfMonths = (unitAbove, aboveTimeBlocks, interval) => {
    if (unitAbove === "month") {
        const dayInfo = [];
        aboveTimeBlocks.forEach((column, index) => {
            const month = (0, time_resolution_1.getMonth)(column);
            const year = (0, time_resolution_1.getYear)(column);
            const currentMonthDays = (0, time_resolution_1.daysInMonth)(Number(month), Number(year));
            if (index === 0) {
                const startDay = (0, time_resolution_1.getStartMonthsDay)(interval.start);
                const daysToMonthEnd = currentMonthDays - Number(startDay) + 1;
                dayInfo.push({
                    thisMonth: daysToMonthEnd,
                    untilNow: daysToMonthEnd,
                });
                return;
            }
            const n = dayInfo[index - 1].untilNow + currentMonthDays;
            dayInfo.push({
                thisMonth: currentMonthDays,
                untilNow: n,
            });
        });
        return dayInfo;
    }
    return [];
};
exports.getDaysNumberOfMonths = getDaysNumberOfMonths;
const getAboveTimeBlocksVisible = (visibleTimeBlocks, aboveTimeBlocks, startUnitAbove, endUnitAbove, arrayIndex) => {
    if (visibleTimeBlocks.length !== 0) {
        const blocksArray = [];
        aboveTimeBlocks.forEach((i, index) => {
            const startMillis = i.start.toMillis();
            const endMillis = i.end.toMillis();
            if (endMillis > startUnitAbove.toMillis() && endMillis <= endUnitAbove.toMillis()) {
                arrayIndex.push(index);
                blocksArray.push(i);
                return;
            }
            if (startMillis >= startUnitAbove.toMillis() && startMillis < endUnitAbove.toMillis()) {
                arrayIndex.push(index);
                blocksArray.push(i);
                return;
            }
        });
        return blocksArray;
    }
    return [];
};
exports.getAboveTimeBlocksVisible = getAboveTimeBlocksVisible;
