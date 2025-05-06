"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getLineData = exports.LINE_OFFSET = exports.LINE_WIDTH = exports.LINE_TENSION = exports.CIRCLE_POINT_STROKE = exports.CIRCLE_POINT_COLOR = exports.LINE_COLOR = exports.CIRCLE_POINT_OFFSET = void 0;
const tasks_1 = require("./tasks");
exports.CIRCLE_POINT_OFFSET = 4;
exports.LINE_COLOR = "rgb(135,133,239)";
exports.CIRCLE_POINT_COLOR = "rgb(141,141,141)";
exports.CIRCLE_POINT_STROKE = "rgb(74,88,97)";
exports.LINE_TENSION = 0.5;
exports.LINE_WIDTH = 2;
exports.LINE_OFFSET = 20;
const getLineData = (connectLine, rowHeight, getTaskXCoordinate, getTaskYCoordinate, type) => {
    const anchorArr = [];
    const workLineArr = [];
    const taskY = type === "back" ? "startResId" : "endResId";
    const taskX = type === "back" ? "start" : "end";
    connectLine.forEach((i) => {
        const anchY = getTaskYCoordinate(+i[taskY], rowHeight) + (rowHeight * tasks_1.TASK_HEIGHT_OFFSET) / 2;
        const anchX = getTaskXCoordinate(i[taskX]);
        anchorArr.push({ x: anchX, y: anchY });
        workLineArr.push(i.id);
    });
    return { anchorArr, workLineArr };
};
exports.getLineData = getLineData;
