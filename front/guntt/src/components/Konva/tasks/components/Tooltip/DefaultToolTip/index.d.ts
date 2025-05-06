import { FC } from "react";
import { Localized } from "../../../../timeline/TimelineContext";
type DefaultToolTip = {
    localized: Localized;
    startDuration: string;
    endDuration: string;
    duration: {
        time: number;
        unit: string;
    };
    completedPercentage?: number;
    percentage: string;
    label: string;
};
declare const DefaultToolTip: FC<DefaultToolTip>;
export default DefaultToolTip;
