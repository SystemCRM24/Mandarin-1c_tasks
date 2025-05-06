import { DateTime, Interval } from "luxon";
import { Scale } from "./time-resolution";
interface VisibleHourInfoProps {
    backHour?: boolean;
    nextHour?: boolean;
}
interface DayDetailProps {
    thisMonth?: number;
    untilNow?: number;
}
export declare const getTimeBlocksTzInfo: (timeBlock: Interval[], initialTz?: string) => VisibleHourInfoProps[];
export declare const getDaysNumberOfMonths: (unitAbove: Scale, aboveTimeBlocks: Interval[], interval: Interval) => DayDetailProps[];
export declare const getAboveTimeBlocksVisible: (visibleTimeBlocks: Interval[], aboveTimeBlocks: Interval[], startUnitAbove: DateTime | null, endUnitAbove: DateTime | null, arrayIndex: number[]) => Interval<boolean>[];
export {};
