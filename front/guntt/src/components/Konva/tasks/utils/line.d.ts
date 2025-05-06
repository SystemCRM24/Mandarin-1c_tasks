import { LineData } from "../../timeline/TimelineContext";
export type LineType = {
    points: number[];
};
export type AnchorPoint = {
    x: number;
    y: number;
};
export declare const CIRCLE_POINT_OFFSET = 4;
export declare const LINE_COLOR = "rgb(135,133,239)";
export declare const CIRCLE_POINT_COLOR = "rgb(141,141,141)";
export declare const CIRCLE_POINT_STROKE = "rgb(74,88,97)";
export declare const LINE_TENSION = 0.5;
export declare const LINE_WIDTH = 2;
export declare const LINE_OFFSET = 20;
export declare const getLineData: (connectLine: LineData[], rowHeight: number, getTaskXCoordinate: (startTime: number) => number, getTaskYCoordinate: (rowIndex: number, rowHeight: number) => number, type: "back" | "front") => {
    anchorArr: AnchorPoint[];
    workLineArr: string[];
};
