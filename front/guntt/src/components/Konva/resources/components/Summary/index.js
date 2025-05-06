"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importDefault(require("react"));
const react_konva_1 = require("react-konva");
const TimelineContext_1 = require("../../../timeline/TimelineContext");
const SummaryHeader_1 = __importDefault(require("../SummaryHeader"));
/**
 * This component renders a Konva layer containing one header for each resource (`Summary`).
 */
const SummaryLayer = () => {
    const { resources } = (0, TimelineContext_1.useTimelineContext)();
    return (react_1.default.createElement(react_konva_1.Layer, null, resources.map((data, index) => {
        const isLast = index === resources.length - 1;
        return react_1.default.createElement(SummaryHeader_1.default, { key: `summary-${data.id}`, index: index, isLast: isLast, id: data.id });
    })));
};
exports.default = SummaryLayer;
