import React, {useCallback, useMemo} from "react";
import { Layer } from "react-konva";
import { KonvaLine, KonvaText } from "../../@konva";

import { useTimelineContext } from "../../timeline/TimelineContext";


interface NowLineProps {
  rowHeight: number;
  stageHeight: number;
  columnWidth: number;
}


const NowLine = ({rowHeight, stageHeight, columnWidth}: NowLineProps) => {
  const {
    interval: { start: intervalStart },
    resolution,
    workTime,
    now,
  } = useTimelineContext();

  const x = useMemo(
    () => {
      let startOffsetInUnit = now.diff(intervalStart!);
      // WorkTime logic
      const nonWorkTimeDiff = workTime.calcOuterNonWorkDuration(now, 'day');
      startOffsetInUnit = startOffsetInUnit.minus(nonWorkTimeDiff);
      // end
      const offset = startOffsetInUnit.as(resolution.unit);
      return (offset * columnWidth) / resolution.sizeInUnits;
    },
    [now, intervalStart, resolution.unit, columnWidth, resolution.sizeInUnits]
  );

  const text = useMemo(
    () => now.toISOTime()?.slice(0, 5),
    [now]
  );

  return (
    <Layer>
      <KonvaLine
        x={x}
        y={rowHeight * 0.8}
        points={[0, 0, 0, stageHeight]}
        stroke="red"
        strokeWidth={1}
        dash={[8, 3]}
      />
      <KonvaText 
        fill="red" 
        x={x} 
        y={rowHeight * 0.8 - 20} 
        text={text} 
        width={columnWidth}
      />
    </Layer>
  );
};

export default NowLine;