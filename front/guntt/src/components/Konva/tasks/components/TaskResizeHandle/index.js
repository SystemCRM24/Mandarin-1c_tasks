"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importStar(require("react"));
const react_konva_1 = require("react-konva");
const TimelineContext_1 = require("../../../timeline/TimelineContext");
const tasks_1 = require("../../utils/tasks");
const TaskResizeHandle = ({ height, onResizeEnd, onResizeMove, onResizeStart, opacity, position, taskId, xCoordinate, }) => {
    const { enableResize } = (0, TimelineContext_1.useTimelineContext)();
    const onDragMove = (0, react_1.useCallback)((e) => onResizeMove(e, position), [onResizeMove, position]);
    const onMouseLeave = (0, react_1.useCallback)((e) => {
        e.cancelBubble = true;
        const stage = e.target.getStage();
        if (!stage || !enableResize) {
            return;
        }
        stage.container().style.cursor = "default";
    }, [enableResize]);
    const onMouseOver = (0, react_1.useCallback)((e) => {
        e.cancelBubble = true;
        const stage = e.target.getStage();
        if (!stage || !enableResize) {
            return;
        }
        const mouseCursor = `${position === "lx" ? "w" : "e"}-resize`;
        stage.container().style.cursor = mouseCursor;
    }, [enableResize, position]);
    const handleId = (0, react_1.useMemo)(() => `${taskId}-resize-${position}`, [position, taskId]);
    return (react_1.default.createElement(react_konva_1.Rect, { id: handleId, draggable: enableResize, fill: "transparent", height: height, onDragStart: onResizeStart, onDragMove: onDragMove, onDragEnd: onResizeEnd, onMouseOver: onMouseOver, onMouseLeave: onMouseLeave, opacity: opacity, width: tasks_1.TASK_BORDER_RADIUS, x: xCoordinate, y: 0 }));
};
exports.default = TaskResizeHandle;
