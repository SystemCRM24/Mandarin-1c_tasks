import React, { useMemo } from "react";
import { Duration, Interval } from "luxon";

import { KonvaGroup, KonvaLine, KonvaText } from "../../@konva";
import { useTimelineContext } from "../../timeline/TimelineContext";
import { DEFAULT_STROKE_DARK_MODE, DEFAULT_STROKE_LIGHT_MODE } from "../../utils/theme";
import { displayAboveInterval } from "../../utils/time-resolution";

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

const GridCellGroup = ({ column, index, dayInfo, hourInfo }: GridCellGroupProps) => {
  const {
    columnWidth,
    resolution: { sizeInUnits, unit, unitAbove },
    rowHeight,
    theme: { color: themeColor },
    dateLocale,
    workTime
  } = useTimelineContext();

  const cellLabel = useMemo(
    () => displayAboveInterval(column, unitAbove, dateLocale!),
    [column, unitAbove, dateLocale]
  );
  
  const points = useMemo(() => [0, 0, 0, rowHeight], [rowHeight]);

  // WorkTime logic
  const daysInInterval = useMemo(() => {
    let count = 0;
    for ( const interval of workTime.intervals ) {
      if ( column.intersection(interval) ) {
        count += 1;
      }
    }
    return count;
  }, [index]);

  const daysBeforeIntevalEnd = useMemo(() => {
    let count = 0;
    for ( const interval of workTime.intervals ) {
      if ( !(interval.isBefore(column.end!)) ) {
        return count;
      }
      count += 1;
    }
    return count;
  }, [index]);
  // end of this shit

  const unitAboveInUnitBelow = useMemo(() => {
    switch ( unitAbove ) {
      case 'day':
        return 9 / sizeInUnits;
      case 'week':
        return Duration.fromObject({ [unitAbove]: 1 }).as(unit) / sizeInUnits / ((24 * 7) / (9 * daysInInterval));
      case 'month':
        return Duration.fromObject({ ["day"]: dayInfo!.thisMonth }).as("week") / sizeInUnits;
      default:
        return Duration.fromObject({ [unitAbove]: 1 }).as(unit) / sizeInUnits;
    }
  }, [sizeInUnits, dayInfo, unitAbove, unit, index]);

  const unitAboveSpanInPx = useMemo(() => {
    return unitAboveInUnitBelow * columnWidth;
  }, [columnWidth, unitAboveInUnitBelow]);

  const xPos = useMemo(() => {
    if (unitAbove === "month") {
      const pxUntil =
        dayInfo!.untilNow !== dayInfo!.thisMonth
          ? Duration.fromObject({ ["day"]: dayInfo!.untilNow! - dayInfo!.thisMonth! }).as("week") / sizeInUnits
          : 0;

      if (hourInfo!.backHour) {
        const hourInMonthPx = columnWidth / 168;
        return pxUntil * columnWidth + unitAboveSpanInPx + hourInMonthPx;
      }

      if (hourInfo!.nextHour) {
        const hourInMonthPx = columnWidth / 168;
        return pxUntil * columnWidth + unitAboveSpanInPx - hourInMonthPx;
      }

      return pxUntil * columnWidth + unitAboveSpanInPx;
    }
    if (unitAbove === "day") {
      if (hourInfo!.backHour) {
        return index * unitAboveSpanInPx + columnWidth / sizeInUnits;
      }

      if (hourInfo!.nextHour) {
        return index * unitAboveSpanInPx - columnWidth / sizeInUnits;
      }
    }
    if (unitAbove === "week") {
      if (hourInfo!.backHour) {
        return index * unitAboveSpanInPx + columnWidth / 24;
      }

      if (hourInfo!.nextHour) {
        return index * unitAboveSpanInPx - columnWidth / 24;
      }
    }
    // let res = index * unitAboveSpanInPx
    switch ( unitAbove ) {
      case 'day':
        return unitAboveSpanInPx * daysInInterval * daysBeforeIntevalEnd;
      case 'week':
      default:
        return unitAboveSpanInPx / daysInInterval * daysBeforeIntevalEnd;
    }
  }, [index, unitAboveSpanInPx, columnWidth, sizeInUnits, dayInfo, unitAbove, hourInfo]);

  const yPos = useMemo(() => rowHeight * 0.3, [rowHeight]);

  const xPosLabel = useMemo(() => {
    if (unitAbove === "month") {
      return xPos - unitAboveSpanInPx;
    }
    if (unitAbove === "day") {
      if (hourInfo!.backHour) {
        return index * unitAboveSpanInPx + columnWidth / sizeInUnits;
      }

      if (hourInfo!.nextHour) {
        return index * unitAboveSpanInPx - columnWidth / sizeInUnits;
      }
    }
    const res = (unitAboveSpanInPx / daysInInterval * daysBeforeIntevalEnd) - unitAboveSpanInPx;
    return res;
  }, [xPos, unitAboveSpanInPx, unitAbove, index, columnWidth, sizeInUnits, hourInfo]);

  const stroke = useMemo(() => {
    if (themeColor === "black") {
      return DEFAULT_STROKE_LIGHT_MODE;
    }
    return DEFAULT_STROKE_DARK_MODE;
  }, [themeColor]);

  return (
    <KonvaGroup key={`timeslot-${index}`}>
      <KonvaLine x={xPos} y={0} points={points} stroke={stroke} strokeWidth={1} />
      <KonvaText
        align="center"
        fill={themeColor}
        x={xPosLabel}
        y={yPos - 8}
        text={xPosLabel !== Infinity ? cellLabel: ''}
        width={unitAboveSpanInPx}
      />
    </KonvaGroup>
  );
};

export default GridCellGroup;
