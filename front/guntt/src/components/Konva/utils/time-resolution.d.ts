import { DateTime, Interval } from "luxon";
export type Scale = "minute" | "hour" | "day" | "week" | "month" | "year";
export type Resolution = "1min" | "5min" | "10min" | "15min" | "30min" | "1hrs" | "2hrs" | "3hrs" | "6hrs" | "12hrs" | "1day" | "1week" | "2weeks";
export type ResolutionData = {
    columnSize: number;
    label: string;
    sizeInUnits: number;
    unit: Scale;
    unitAbove: Scale;
};
export declare const RESOLUTIONS: Resolution[];
/**
 * Util to display an interval in a human readable format
 * @param interval the interval to display
 * @param unit the unit in which to display the interval
 */
export declare const displayAboveInterval: (interval: Interval, unit: Scale, locale: string) => string;
export declare const getMonth: (interval: Interval) => string;
export declare const getYear: (interval: Interval) => string;
export declare const getStartMonthsDay: (start: DateTime) => string;
export declare const daysInMonth: (month: number, year: number) => number;
/**
 * Util to display an interval in a human readable format
 * @param interval the interval to display
 * @param unit the unit in which to display the interval
 */
export declare const displayInterval: (interval: Interval, unit: Scale, locale: string) => string;
/**
 * Gets the resolution data for the given key
 * @param key key of the resolution to get
 */
export declare const getResolutionData: (key: Resolution) => ResolutionData;
