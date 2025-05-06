import React, { PropsWithChildren } from "react";
import { DateTime, Interval } from "luxon";
import { Resource } from "../resources/utils/resources";
import { AreaSelect, TaskData } from "../tasks/utils/tasks";
import { InternalTimeRange } from "../utils/time";
import { Resolution, ResolutionData } from "../utils/time-resolution";
import { TimelineInput } from "../utils/timeline";
import { WorkTime } from "../utils/workTime";
import { KonvaTimelineError } from "..";
declare global {
    interface Window {
        __MELFORE_KONVA_TIMELINE_DEBUG__?: boolean;
    }
}
type TimelineThemeMode = "dark" | "light";
export type Localized = {
    start: string;
    end: string;
    duration: string;
    completed: string;
};
export type CustomToolTipData = TaskData & {
    start: string;
    end: string;
};
export type LineData = {
    id: string;
    startId: string;
    endId: string;
    startResId: string;
    endResId: string;
    start: number;
    end: number;
};
export type CustomRes = {
    resource: Resource;
    dimension: {
        width: number;
        height: number;
    };
};
type taskChangeOpts = {
    tasksId?: string[];
    addTime?: number;
    coords?: {
        x: number;
        y: number;
    };
};
export type TimelineProviderProps = PropsWithChildren<TimelineInput> & {
    /**
     * Enables debug logging in browser console
     */
    debug?: boolean;
    /**
     * Enables drag&drop operation on tasks
     */
    enableDrag?: boolean;
    /**
     * Enables resize operation on tasks
     */
    enableResize?: boolean;
    /**
     * Label to display in header column
     */
    headerLabel?: string;
    /**
     * Initial date time to scroll to
     */
    initialDateTime?: number | string;
    /**
     * Callback invoked when errors are thrown
     */
    onErrors?: (errors: KonvaTimelineError[]) => void;
    /**
     * Event handler for task click
     */
    onTaskClick?: (task: TaskData) => void;
    /**
     * Event handler for task change event (drag and resize)
     */
    onTaskChange?: (task: TaskData, opts?: taskChangeOpts) => void;
    /**
     * Timezone used for display (defaults to 'system')
     */
    timezone?: string;
    /**
     * Theme color in use
     */
    theme?: TimelineThemeMode;
    /**
     * ToolTips Labels
     */
    localized?: Localized;
    /**
     * Language used for date format
     */
    dateLocale?: string;
    /**
     * Event handler for task add event
     */
    onAreaSelect?: (task: AreaSelect) => void;
    /**
     * ToolTip display
     */
    toolTip?: boolean;
    /**
     * Callback that return a personalized tooltip( 200x100 is max possible size)
     */
    customToolTip?: (taskData: CustomToolTipData) => React.JSX.Element;
    /**
     * Enables pattern for incomplete part of the task (default true)
     */
    enableTaskPattern?: boolean;
    /**
     * Enables connection between tasks (if kLine is set in taskData)
     */
    enableLines?: boolean;
    /**
     * Event handler for resource click
     */
    onResourceClick?: (task: Resource) => void;
    /**
     * Summary data
     */
    summary?: {
        id: string;
        label: string;
    }[];
    /**
     * Enable summary
     */
    showSummary?: boolean;
    /**
     * Header label to display in summary column, default is Summary
     */
    summaryHeader?: string;
    /**
     * Callback that return a personalized resources(this func return also the dimension of a single resourse)
     */
    customResources?: (resourceData: CustomRes) => React.JSX.Element;
};
type TimelineTheme = {
    color: string;
};
type TimelineContextType = Required<Pick<TimelineInput, "columnWidth" | "displayTasksLabel" | "hideResources" | "resources" | "rowHeight">> & {
    aboveTimeBlocks: Interval[];
    blocksOffset: number;
    dragResolution: ResolutionData;
    drawRange: InternalTimeRange;
    enableDrag: boolean;
    enableResize: boolean;
    headerLabel?: string;
    initialDateTime?: number;
    interval: Interval;
    onErrors?: (errors: KonvaTimelineError[]) => void;
    onTaskClick?: (task: TaskData) => void;
    onTaskChange?: (task: TaskData, opts?: taskChangeOpts) => void;
    resolution: ResolutionData;
    resolutionKey: Resolution;
    resourcesContentHeight: number;
    setDrawRange: (range: InternalTimeRange) => void;
    tasks: TaskData<InternalTimeRange>[];
    theme: TimelineTheme;
    timeBlocks: Interval[];
    timezone: string;
    visibleTimeBlocks: Interval[];
    localized: Localized;
    dateLocale?: string;
    onAreaSelect?: (task: AreaSelect) => void;
    toolTip?: boolean;
    customToolTip?: (taskData: CustomToolTipData) => React.JSX.Element;
    enableTaskPattern?: boolean;
    enableLines?: boolean;
    validLine?: LineData[];
    allValidTasks: TaskData<InternalTimeRange>[];
    externalRangeInMillis: InternalTimeRange;
    onResourceClick?: (resource: Resource) => void;
    summary?: {
        id: string;
        label: string;
    }[];
    showSummary?: boolean;
    summaryWidth: number;
    summaryHeader?: string;
    customResources?: (resourceData: CustomRes) => React.JSX.Element;
    workTime: WorkTime;
    now: DateTime;
};
export declare const TimelineProvider: ({ children, columnWidth: externalColumnWidth, debug, displayTasksLabel, dragResolution: externalDragResolution, enableDrag, enableResize, headerLabel, hideResources, initialDateTime: externalInitialDateTime, onErrors, onTaskClick, onTaskChange, tasks: externalTasks, range: externalRange, resolution: externalResolution, resources: externalResources, rowHeight: externalRowHeight, timezone: externalTimezone, theme: externalTheme, localized, dateLocale, onAreaSelect, toolTip, customToolTip, enableTaskPattern, enableLines, onResourceClick, summary: externalSummary, showSummary, summaryHeader, customResources, workIntervals, isoNow, }: TimelineProviderProps) => React.JSX.Element;
export declare const useTimelineContext: () => TimelineContextType;
export {};
