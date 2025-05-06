import { FC } from "react";
import { KonvaPoint } from "../../../utils/konva";
import { TaskData } from "../../utils/tasks";
export interface TaskTooltipProps extends KonvaPoint {
    task: TaskData;
}
/**
 * This component renders a task tooltip inside a canvas.
 */
declare const TaskTooltip: FC<TaskTooltipProps>;
export default TaskTooltip;
