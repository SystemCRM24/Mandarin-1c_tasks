"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importDefault(require("react"));
const react_konva_1 = require("react-konva");
const TimelineContext_1 = require("../../../timeline/TimelineContext");
const Header_1 = __importDefault(require("../Header"));
/**
 * This component renders a Konva layer containing one header for each resource (`ResourceHeader`).
 */
const ResourcesLayer = () => {
    const { resources } = (0, TimelineContext_1.useTimelineContext)();
    return (react_1.default.createElement(react_konva_1.Layer, null, resources.map((resource, index) => {
        const isLast = index === resources.length - 1;
        const header = index === 0 ? true : false;
        return (react_1.default.createElement(Header_1.default, { key: `resource-${resource.id}`, index: index, isLast: isLast, resource: resource, header: header }));
    })));
};
exports.default = ResourcesLayer;
