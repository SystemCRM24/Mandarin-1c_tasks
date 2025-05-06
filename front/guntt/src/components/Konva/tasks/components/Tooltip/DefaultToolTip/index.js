"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importDefault(require("react"));
const DefaultToolTip = ({ localized, startDuration, endDuration, duration, completedPercentage, percentage, label, }) => {
    return (react_1.default.createElement("div", { style: {
            backgroundColor: "white",
            border: "ridge",
            borderColor: "black",
            borderWidth: "1px",
            padding: 8,
            boxShadow: "2px 2px 8px black",
            maxWidth: 251,
            overflow: "hidden",
            textOverflow: "ellipsis",
        } },
        react_1.default.createElement("b", { style: {
                fontFamily: "Times New Roman",
                fontSize: 16,
                fontWeight: 700,
                whiteSpace: "pre-line"
            } }, label),
        react_1.default.createElement("br", null),
        react_1.default.createElement("div", { style: { display: "inline-flex", alignItems: "center" } },
            react_1.default.createElement("b", { style: { fontSize: 14, fontFamily: "Times New Roman", fontWeight: 700 } },
                localized.start,
                ": "),
            "\u00A0\u00A0\u00A0",
            react_1.default.createElement("span", { style: { fontFamily: "Courier New", fontSize: 13 } }, startDuration)),
        react_1.default.createElement("br", null),
        react_1.default.createElement("div", { style: { display: "inline-flex", alignItems: "center" } },
            react_1.default.createElement("b", { style: { fontSize: 14, fontFamily: "Times New Roman", fontWeight: 700 } },
                localized.end,
                ": "),
            "\u00A0\u00A0\u00A0",
            react_1.default.createElement("span", { style: { fontFamily: "Courier New", fontSize: 13 } }, endDuration)),
        react_1.default.createElement("br", null),
        react_1.default.createElement("div", { style: { display: "inline-flex", alignItems: "center" } },
            react_1.default.createElement("b", { style: { fontFamily: "Times New Roman", fontSize: 14, fontWeight: 700 } },
                localized.duration,
                ": "),
            "\u00A0\u00A0\u00A0",
            react_1.default.createElement("span", { style: { fontFamily: "Courier New", fontSize: 13 } },
                duration.time,
                " ",
                duration.unit,
                "(s)")),
        react_1.default.createElement("br", null),
        completedPercentage && (react_1.default.createElement("div", { style: { display: "inline-flex", alignItems: "center" } },
            react_1.default.createElement("b", { style: { fontFamily: "Times New Roman", fontSize: 14, fontWeight: 700 } },
                localized.completed,
                ": "),
            "\u00A0\u00A0\u00A0",
            react_1.default.createElement("span", { style: { fontFamily: "Courier New", fontSize: 13 } }, percentage)))));
};
exports.default = DefaultToolTip;
