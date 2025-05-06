import { Interval } from "luxon";
import { Operation } from "../../utils/operations";
import { InternalTimeRange, TimeRange, TimeInput } from "../../utils/time";
import { ResolutionData } from "../../utils/time-resolution";
export interface TaskData<T extends TimeRange = TimeRange> {
    /**
     * Unique identifier of the task
     */
    id: string;
    /**
     * Label of the task
     */
    label: string;
    /**
     * Description of the task
     */
    description?: string;
    /**
     * Id of assigned resource
     */
    resourceId: string;
    /**
     * Completed Percentage
     */
    completedPercentage?: number;
    /**
     * Task time range
     */
    time: T;
    /**
     * Deadline of this task
     */
    deadline: TimeInput;
    /**
     * Id of connected Tasks
     */
    relatedTasks?: string[];
}
type FilteredTasks = Operation<TaskData<InternalTimeRange>>;
export type TaskDimensions = {
    row: number;
    width: number;
    x: number;
    y: number;
    handler?: string;
};
export type AreaSelect = {
    resourceId: string;
    range: TimeRange;
};
export declare const TASK_OFFSET_Y = 0.15;
export declare const TASK_BORDER_RADIUS = 4;
export declare const TASK_HEIGHT_OFFSET = 0.7;
/**
 * Gets task Y coordinate
 * @param rowIndex the row index
 * @param rowHeight the row height
 */
export declare const getTaskYCoordinate: (rowIndex: number, rowHeight: number) => number;
/**
 * Filters valid tasks to be shown in the chart
 * @param tasks list of tasks as passed to the component
 * @param intervals intervals as passed to the component
 */
export declare const validateTasks: (tasks: TaskData[], range: InternalTimeRange | null, timezone: string | undefined) => FilteredTasks;
/**
 * Filters valid tasks to be shown in the chart
 * @param tasks list of tasks as passed to the component
 * @param intervals intervals as passed to the component
 */
export declare const filterTasks: (tasks: TaskData<InternalTimeRange>[], range: InternalTimeRange | null) => TaskData<InternalTimeRange>[];
export declare const lineFilter: (tasks: TaskData<InternalTimeRange>[], range: InternalTimeRange | null) => TaskData<InternalTimeRange>[];
export declare const onEndTimeRange: (taskDimesion: TaskDimensions, resolution: ResolutionData, columnWidth: number, interval: Interval) => TimeRange;
export declare const connectedTasks: (taskData: TaskData, allValidTasks: TaskData[], addTime: number, range: InternalTimeRange) => {
    allKLine: string[];
    maxAddTime: number;
};
export {};
