"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.KonvaText = exports.KonvaRect = exports.KonvaLine = exports.KonvaLayer = exports.KonvaGroup = void 0;
const react_1 = __importDefault(require("react"));
const react_konva_1 = require("react-konva");
const KonvaGroup = (props) => {
    return react_1.default.createElement(react_konva_1.Group, Object.assign({}, props, { listening: false, perfectDrawEnabled: false }));
};
exports.KonvaGroup = KonvaGroup;
const KonvaLayer = (props) => {
    return react_1.default.createElement(react_konva_1.Layer, Object.assign({}, props, { listening: false, perfectDrawEnabled: false }));
};
exports.KonvaLayer = KonvaLayer;
const KonvaLine = (props) => {
    return react_1.default.createElement(react_konva_1.Line, Object.assign({}, props, { listening: false, perfectDrawEnabled: false }));
};
exports.KonvaLine = KonvaLine;
const KonvaRect = (props) => {
    return react_1.default.createElement(react_konva_1.Rect, Object.assign({}, props, { listening: false, perfectDrawEnabled: false }));
};
exports.KonvaRect = KonvaRect;
const KonvaText = (props) => {
    return react_1.default.createElement(react_konva_1.Text, Object.assign({}, props, { listening: false, perfectDrawEnabled: false }));
};
exports.KonvaText = KonvaText;
