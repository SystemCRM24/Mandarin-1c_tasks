"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importDefault(require("react"));
const react_konva_1 = require("react-konva");
const line_1 = require("../../utils/line");
const LineKonva = ({ points }) => {
    return (react_1.default.createElement(react_konva_1.Group, null,
        react_1.default.createElement(react_konva_1.Line, { strokeWidth: line_1.LINE_WIDTH, lineJoin: "round", stroke: line_1.LINE_COLOR, points: points, tension: line_1.LINE_TENSION }),
        react_1.default.createElement(react_konva_1.Circle, { x: points[0] + line_1.CIRCLE_POINT_OFFSET, y: points[1], radius: 4, stroke: line_1.CIRCLE_POINT_STROKE, fill: line_1.CIRCLE_POINT_COLOR, strokeWidth: 1 }),
        react_1.default.createElement(react_konva_1.Circle, { x: points[6] - line_1.CIRCLE_POINT_OFFSET, y: points[7], radius: 4, stroke: line_1.CIRCLE_POINT_STROKE, fill: line_1.CIRCLE_POINT_COLOR, strokeWidth: 1 })));
};
exports.default = LineKonva;
