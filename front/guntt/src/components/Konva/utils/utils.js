"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.executeWithPerfomanceCheck = void 0;
const luxon_1 = require("luxon");
const logger_1 = require("./logger");
const executeWithPerfomanceCheck = (tag, item, fn) => {
    if (window.__MELFORE_KONVA_TIMELINE_DEBUG__) {
        (0, logger_1.logDebug)(tag, `Running ${item}`);
        const start = luxon_1.DateTime.now().toMillis();
        const fnResult = fn();
        const end = luxon_1.DateTime.now().toMillis();
        (0, logger_1.logDebug)(tag, `${item} calculation took ${end - start} ms`);
        return fnResult;
    }
    const result = fn();
    return result;
};
exports.executeWithPerfomanceCheck = executeWithPerfomanceCheck;
