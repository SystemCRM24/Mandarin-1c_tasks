"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importDefault(require("react"));
const timeline_1 = __importDefault(require("../timeline"));
const TimelineContext_1 = require("../timeline/TimelineContext");
const KonvaTimeline = (props) => {
    return (react_1.default.createElement(TimelineContext_1.TimelineProvider, Object.assign({}, props),
        react_1.default.createElement(timeline_1.default, null)));
};
exports.default = KonvaTimeline;
