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
exports.SummaryHeaderDocs = void 0;
const react_1 = __importStar(require("react"));
const react_konva_1 = require("react-konva");
const _konva_1 = require("../../../@konva");
const TimelineContext_1 = require("../../../timeline/TimelineContext");
const dimensions_1 = require("../../../utils/dimensions");
const theme_1 = require("../../../utils/theme");
/**
 * This component renders a resource header. It displays a text (`resource.label`) and a delimiter line.
 */
const SummaryHeader = ({ index, isLast = false, id }) => {
    const { rowHeight, theme: { color: themeColor }, summaryWidth, summary, summaryHeader,
    //onResourceClick,
     } = (0, TimelineContext_1.useTimelineContext)();
    const rowPoints = (0, react_1.useMemo)(() => [0, rowHeight, summaryWidth, rowHeight], [rowHeight, summaryWidth]);
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
    const konvaText = (0, react_1.useMemo)(() => {
        if (!summary) {
            return "🚫";
        }
        if (index === 0) {
            return summaryHeader ? summaryHeader : summary[0].label;
        }
        const data = summary.find((i) => i.id === id);
        if (!data) {
            return "🚫";
        }
        return data.label;
    }, [summary, id, index, summaryHeader]);
    /*const onClick = useCallback(
      () => onResourceClick && !header && onResourceClick(resource),
      [resource, header, onResourceClick]
    );*/
    return (react_1.default.createElement(react_konva_1.Group, { y: yCoordinate },
        react_1.default.createElement(react_konva_1.Rect, { width: summaryWidth, height: rowHeight }),
        react_1.default.createElement(_konva_1.KonvaText, { fill: themeColor, fontSize: dimensions_1.DEFAULT_TEXT_SIZE, height: rowHeight, width: summaryWidth, text: konvaText, verticalAlign: "middle", align: "center", ellipsis: true, wrap: "none" }),
        !isLast && (react_1.default.createElement(react_konva_1.Group, null,
            react_1.default.createElement(_konva_1.KonvaLine, { points: rowPoints, stroke: stroke }),
            react_1.default.createElement(_konva_1.KonvaRect, { x: 0, y: rowHeight, width: summaryWidth, height: rowHeight, fill: fill })))));
};
exports.SummaryHeaderDocs = SummaryHeader;
exports.default = (0, react_1.memo)(SummaryHeader);
