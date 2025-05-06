import { FC } from "react";
import { TaskTooltipProps } from "../Tooltip";
interface TasksLayerProps {
    taskTooltip: TaskTooltipProps | null;
    setTaskTooltip: (tooltip: TaskTooltipProps | null) => void;
    create?: boolean;
    onTaskEvent: (value: boolean) => void;
}
/**
 * This component renders a set of tasks as a Konva Layer.
 * Tasks are displayed accordingly to their assigned resource (different vertical / row position) and their timing (different horizontal / column position)
 * `TasksLayer` is also responsible of handling callback for task components offering base implementation for click, leave and over.
 *
 * The playground has a canvas that simulates 1 day of data with 1 hour resolution.
 * Depending on your screen size you might be able to test also the horizontal scrolling behaviour.
 */
declare const LayerLine: FC<TasksLayerProps>;
export default LayerLine;
