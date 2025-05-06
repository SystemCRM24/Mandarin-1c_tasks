import React from "react";
import { Interval } from "luxon";
interface GridCellGroupProps {
    column: Interval;
    index: number;
    dayInfo?: {
        thisMonth?: number;
        untilNow?: number;
    };
    hourInfo?: {
        backHour?: boolean;
        nextHour?: boolean;
    };
}
declare const GridCellGroup: ({ column, index, dayInfo, hourInfo }: GridCellGroupProps) => React.JSX.Element;
export default GridCellGroup;
