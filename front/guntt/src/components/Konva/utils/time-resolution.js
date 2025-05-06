"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getResolutionData = exports.displayInterval = exports.daysInMonth = exports.getStartMonthsDay = exports.getYear = exports.getMonth = exports.displayAboveInterval = exports.RESOLUTIONS = void 0;
const dimensions_1 = require("./dimensions");
const RESOLUTIONS_DATA = {
    "1min": {
        columnSize: dimensions_1.DEFAULT_GRID_COLUMN_WIDTH / 2,
        label: "1 Minute",
        sizeInUnits: 1,
        unit: "minute",
        unitAbove: "hour",
    },
    "5min": {
        columnSize: dimensions_1.DEFAULT_GRID_COLUMN_WIDTH / 2,
        label: "5 Minutes",
        sizeInUnits: 5,
        unit: "minute",
        unitAbove: "hour",
    },
    "10min": {
        columnSize: dimensions_1.DEFAULT_GRID_COLUMN_WIDTH / 2,
        label: "10 Minutes",
        sizeInUnits: 10,
        unit: "minute",
        unitAbove: "hour",
    },
    "15min": {
        columnSize: dimensions_1.DEFAULT_GRID_COLUMN_WIDTH,
        label: "15 Minutes",
        sizeInUnits: 15,
        unit: "minute",
        unitAbove: "hour",
    },
    "30min": {
        columnSize: dimensions_1.DEFAULT_GRID_COLUMN_WIDTH,
        label: "30 Minutes",
        sizeInUnits: 30,
        unit: "minute",
        unitAbove: "hour",
    },
    "1hrs": {
        columnSize: dimensions_1.DEFAULT_GRID_COLUMN_WIDTH,
        label: "1 Hour",
        sizeInUnits: 1,
        unit: "hour",
        unitAbove: "day",
    },
    "2hrs": {
        columnSize: dimensions_1.DEFAULT_GRID_COLUMN_WIDTH,
        label: "2 Hours",
        sizeInUnits: 2,
        unit: "hour",
        unitAbove: "day",
    },
    "3hrs": {
        columnSize: dimensions_1.DEFAULT_GRID_COLUMN_WIDTH,
        label: "3 Hours",
        sizeInUnits: 3,
        unit: "hour",
        unitAbove: "day",
    },
    "6hrs": {
        columnSize: dimensions_1.DEFAULT_GRID_COLUMN_WIDTH * 2,
        label: "1/4 of Day",
        sizeInUnits: 6,
        unit: "hour",
        unitAbove: "day",
    },
    "12hrs": {
        columnSize: dimensions_1.DEFAULT_GRID_COLUMN_WIDTH * 3,
        label: "1/2 of Day",
        sizeInUnits: 12,
        unit: "hour",
        unitAbove: "day",
    },
    "1day": {
        columnSize: dimensions_1.DEFAULT_GRID_COLUMN_WIDTH * 3,
        label: "1 Day",
        sizeInUnits: 1,
        unit: "day",
        unitAbove: "week",
    },
    "1week": {
        columnSize: dimensions_1.DEFAULT_GRID_COLUMN_WIDTH * 10,
        label: "1 Week",
        sizeInUnits: 1,
        unit: "week",
        unitAbove: "month",
    },
    "2weeks": {
        columnSize: dimensions_1.DEFAULT_GRID_COLUMN_WIDTH * 10,
        label: "2 Weeks",
        sizeInUnits: 2,
        unit: "week",
        unitAbove: "month",
    },
};
exports.RESOLUTIONS = [
    "1min",
    "5min",
    "10min",
    "15min",
    "30min",
    "1hrs",
    "2hrs",
    "3hrs",
    "6hrs",
    "12hrs",
    "1day",
    "1week",
    "2weeks",
];
/**
 * Util to display an interval in a human readable format
 * @param interval the interval to display
 * @param unit the unit in which to display the interval
 */
const displayAboveInterval = (interval, unit, locale) => {
    const { start } = interval;
    if (!start) {
        return "-";
    }
    switch (unit) {
        case "minute":
        case "hour":
            return start.setLocale(locale).toFormat("dd/MM/yy HH:mm");
        case "day":
            return start.setLocale(locale).toFormat("DDDD");
        case "week":
            return `${start.setLocale(locale).toFormat("MMMM yyyy")} CW ${start.toFormat("WW")}`;
        case "month":
            return start.setLocale(locale).toFormat("MMMM yyyy");
        default:
            return "N/A";
    }
};
exports.displayAboveInterval = displayAboveInterval;
const getMonth = (interval) => {
    const { start } = interval;
    if (!start) {
        return "-";
    }
    return start.toFormat("M");
};
exports.getMonth = getMonth;
const getYear = (interval) => {
    const { start } = interval;
    if (!start) {
        return "-";
    }
    return start.toFormat("yyyy");
};
exports.getYear = getYear;
const getStartMonthsDay = (start) => {
    if (!start) {
        return "-";
    }
    return start.toFormat("d");
};
exports.getStartMonthsDay = getStartMonthsDay;
const daysInMonth = (month, year) => {
    return new Date(year, month, 0).getDate();
};
exports.daysInMonth = daysInMonth;
/**
 * Util to display an interval in a human readable format
 * @param interval the interval to display
 * @param unit the unit in which to display the interval
 */
const displayInterval = (interval, unit, locale) => {
    const { start } = interval;
    if (!start) {
        return "-";
    }
    switch (unit) {
        case "minute":
            return start.setLocale(locale).toFormat("mm");
        case "hour":
            return start.setLocale(locale).toFormat("HH:mm");
        case "day":
            return start.setLocale(locale).toFormat("ccc dd");
        case "week":
            return `CW ${start.setLocale(locale).toFormat("WW")}`;
        case "month":
            return start.setLocale(locale).toFormat("MMM yyyy");
        default:
            return "N/A";
    }
};
exports.displayInterval = displayInterval;
/**
 * Gets the resolution data for the given key
 * @param key key of the resolution to get
 */
const getResolutionData = (key) => RESOLUTIONS_DATA[key];
exports.getResolutionData = getResolutionData;
