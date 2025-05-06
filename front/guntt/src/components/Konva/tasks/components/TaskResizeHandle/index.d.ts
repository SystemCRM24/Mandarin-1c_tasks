import React from "react";
import { KonvaEventObject } from "konva/lib/Node";
interface TaskResizeHandleProps {
    height: number;
    onResizeStart: (e: KonvaEventObject<DragEvent>) => void;
    onResizeMove: (e: KonvaEventObject<DragEvent>, position: "lx" | "rx") => void;
    onResizeEnd: (e: KonvaEventObject<DragEvent>) => void;
    opacity: number;
    position: "lx" | "rx";
    taskId: string;
    xCoordinate: number;
}
declare const TaskResizeHandle: ({ height, onResizeEnd, onResizeMove, onResizeStart, opacity, position, taskId, xCoordinate, }: TaskResizeHandleProps) => React.JSX.Element;
export default TaskResizeHandle;
