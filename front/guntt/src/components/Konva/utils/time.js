"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getXCoordinateFromTime = exports.getIntervalFromInternalTimeRange = exports.isValidRangeTime = exports.getValidRangeTime = exports.getValidTime = void 0;
const luxon_1 = require("luxon");
const logger_1 = require("./logger");
/**
 * Returns valid date based on input, otherwise now
 * @param date the input date (number or string formats)
 */
const getValidTime = (date, timezone) => {
    const tz = timezone || "system";
    let dateInMillis;
    switch (typeof date) {
        case "number":
            dateInMillis = date;
            break;
        case "string":
            dateInMillis = luxon_1.DateTime.fromISO(date, { zone: tz }).toMillis();
            break;
        case "object":
            dateInMillis = luxon_1.DateTime.fromJSDate(date, { zone: tz }).toMillis();
            break;
    }
    return dateInMillis;
};
exports.getValidTime = getValidTime;
const getValidRangeTime = (date, timezone) => {
    const tz = timezone || "system";
    const validDate = new Date(date);
    const dateInMillis = luxon_1.DateTime.fromJSDate(validDate, { zone: tz }).toMillis();
    return dateInMillis;
};
exports.getValidRangeTime = getValidRangeTime;
const isValidRangeTime = (date, name) => {
    const validDate = new Date(date);
    const isValidDateTime = luxon_1.DateTime.fromJSDate(validDate).isValid;
    if (isValidDateTime) {
        return true;
    }
    (0, logger_1.logError)(name, "Invalid Date");
    return false;
};
exports.isValidRangeTime = isValidRangeTime;
/**
 * Converts a TimeRange to a luxon Interval
 * @param range TimeRange to convert
 */
const getIntervalFromInternalTimeRange = ({ start, end }, resolution, timezone) => {
    const tz = timezone || "system";
    const startDateTime = luxon_1.DateTime.fromMillis(start, { zone: tz }).startOf(resolution.unitAbove !== "month" ? resolution.unitAbove : resolution.unit);
    const endDateTime = luxon_1.DateTime.fromMillis(end, { zone: tz }).endOf(resolution.unitAbove !== "month" ? resolution.unitAbove : resolution.unit);
    return luxon_1.Interval.fromDateTimes(startDateTime, endDateTime);
};
exports.getIntervalFromInternalTimeRange = getIntervalFromInternalTimeRange;
const getXCoordinateFromTime = (sizePx, resolution, columnWidth, interval) => {
    const timeOffset = (sizePx * resolution.sizeInUnits) / columnWidth;
    const start = interval.start.plus({ [resolution.unit]: timeOffset }).toMillis();
    return start;
};
exports.getXCoordinateFromTime = getXCoordinateFromTime;
