import React from "react";
import { KonvaDrawable, KonvaPoint } from "../../../utils/konva";
import { TaskData } from "../../utils/tasks";
type TaskMouseEventHandler = (taskId: string, point: KonvaPoint) => void;
type TaskProps = KonvaDrawable & KonvaPoint & {
    /**
     * Task data (id, label, resourceId, time)
     */
    data: TaskData;
    /**
     * On mouse leave event handler
     */
    onLeave: TaskMouseEventHandler;
    /**
     * On mouse over event handler
     */
    onOver: TaskMouseEventHandler;
    /**
     * The width of the task
     */
    width: number;
    /**
     * Prop that indicate disabled item
     */
    disabled?: boolean;
    /**
     * Prop that indicate an event is executing
     */
    onTaskEvent: (value: boolean) => void;
    workLine: (id: string[]) => void;
};
export declare const TaskDocs: ({ data, fill, onLeave, onOver, x, y, width, fillToComplete, disabled, onTaskEvent, workLine, }: TaskProps) => React.JSX.Element;
declare const _default: React.MemoExoticComponent<({ data, fill, onLeave, onOver, x, y, width, fillToComplete, disabled, onTaskEvent, workLine, }: TaskProps) => React.JSX.Element>;
export default _default;
