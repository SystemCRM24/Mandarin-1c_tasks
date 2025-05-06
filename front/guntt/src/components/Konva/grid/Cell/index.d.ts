import React from "react";
import { Interval } from "luxon";
interface GridCellProps {
    column: Interval;
    height: number;
    index: number;
    hourInfo: {
        backHour?: boolean;
        nextHour?: boolean;
    };
}
declare const _default: React.MemoExoticComponent<({ column, height, index, hourInfo: visibleDayInfo }: GridCellProps) => React.JSX.Element>;
export default _default;
