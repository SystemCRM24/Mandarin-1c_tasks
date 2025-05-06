import { Interval } from "luxon";
import { ResolutionData } from "./time-resolution";
export type TimeInput = number | string | Date;
export interface TimeRange {
    /**
     * Start of time range interval
     */
    start: TimeInput;
    /**
     * End of time range interval
     */
    end: TimeInput;
}
export interface InternalTimeRange {
    start: number;
    end: number;
}
/**
 * Returns valid date based on input, otherwise now
 * @param date the input date (number or string formats)
 */
export declare const getValidTime: (date: TimeInput, timezone: string | undefined) => number;
export declare const getValidRangeTime: (date: TimeInput, timezone: string | undefined) => number;
export declare const isValidRangeTime: (date: TimeInput, name: string) => boolean;
/**
 * Converts a TimeRange to a luxon Interval
 * @param range TimeRange to convert
 */
export declare const getIntervalFromInternalTimeRange: ({ start, end }: InternalTimeRange, resolution: ResolutionData, timezone: string | undefined) => Interval;
export declare const getXCoordinateFromTime: (sizePx: number, resolution: ResolutionData, columnWidth: number, interval: Interval) => number;
