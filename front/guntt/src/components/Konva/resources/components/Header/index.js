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
exports.ResourceHeaderDocs = void 0;
const react_1 = __importStar(require("react"));
const react_konva_1 = require("react-konva");
const react_konva_utils_1 = require("react-konva-utils");
const _konva_1 = require("../../../@konva");
const TimelineContext_1 = require("../../../timeline/TimelineContext");
const dimensions_1 = require("../../../utils/dimensions");
const theme_1 = require("../../../utils/theme");
const resources_1 = require("../../utils/resources");
/**
 * This component renders a resource header. It displays a text (`resource.label`) and a delimiter line.
 */
const ResourceHeader = ({ index, isLast = false, resource, header }) => {
    const { rowHeight, theme: { color: themeColor }, onResourceClick, customResources, } = (0, TimelineContext_1.useTimelineContext)();
    const rowPoints = (0, react_1.useMemo)(() => [0, rowHeight, resources_1.RESOURCE_HEADER_WIDTH, rowHeight], [rowHeight]);
    const yCoordinate = (0, react_1.useMemo)(() => rowHeight * index, [index, rowHeight]);
    const fill = (0, react_1.useMemo)(() => {
        if (themeColor === "black") {
            return index % 2 === 0 ? theme_1.DEFAULT_ROW_LIGHT_MODE : theme_1.ALTERNATIVE_ROW;
        }
        return index % 2 === 0 ? theme_1.DEFAULT_ROW_DARK_MODE : theme_1.ALTERNATIVE_ROW;
    }, [index, themeColor]);
    const stroke = (0, react_1.useMemo)(() => {
        if (themeColor === "black") {
            return theme_1.DEFAULT_STROKE_LIGHT_MODE;
        }
        return theme_1.DEFAULT_STROKE_DARK_MODE;
    }, [themeColor]);
    const onClick = (0, react_1.useCallback)(() => onResourceClick && !header && onResourceClick(resource), [resource, header, onResourceClick]);
    const resData = (0, react_1.useMemo)(() => {
        return { resource, dimension: { width: resources_1.RESOURCE_HEADER_WIDTH, height: rowHeight } };
    }, [resource, rowHeight]);
    return (react_1.default.createElement(react_konva_1.Group, { y: yCoordinate },
        react_1.default.createElement(react_konva_1.Rect, { onClick: onClick, width: resources_1.RESOURCE_HEADER_WIDTH, height: rowHeight }),
        customResources && !header ? (react_1.default.createElement(react_konva_utils_1.Html, null, react_1.default.createElement("div", { style: {
                width: resources_1.RESOURCE_HEADER_WIDTH,
                height: rowHeight,
                objectFit: "contain",
                overflow: "hidden",
            } }, customResources(resData)))) : (react_1.default.createElement(_konva_1.KonvaText, { fill: themeColor, fontSize: dimensions_1.DEFAULT_TEXT_SIZE, height: rowHeight, text: resource.label, verticalAlign: "middle", x: resources_1.RESOURCE_TEXT_OFFSET })),
        !isLast && (react_1.default.createElement(react_konva_1.Group, null,
            react_1.default.createElement(_konva_1.KonvaLine, { points: rowPoints, stroke: stroke }),
            react_1.default.createElement(_konva_1.KonvaRect, { x: 0, y: rowHeight, width: resources_1.RESOURCE_HEADER_WIDTH, height: rowHeight, fill: fill })))));
};
exports.ResourceHeaderDocs = ResourceHeader;
exports.default = (0, react_1.memo)(ResourceHeader);
