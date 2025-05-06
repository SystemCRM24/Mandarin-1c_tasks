"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.logWarn = exports.logError = exports.logDebug = void 0;
const TAG = "[@melfore/konva-timeline]";
/**
 * Logs message for given level and component
 * @param level the level of the message to log (e.g. "error")
 * @param component the component subject of the log
 * @param message the message of the log
 */
const logger = (level, component, message) => {
    const text = `${TAG} ${component} - ${message}`;
    switch (level) {
        case "debug":
            // eslint-disable-next-line no-console
            console.info(text);
            return;
        case "error":
            console.error(text);
            return;
        case "warn":
            console.warn(text);
            return;
    }
};
/**
 * Logs message for info level and component only if debug mode enabled
 * @param component the component subject of the log
 * @param message the message of the log
 */
const logDebug = (component, message) => {
    if (!window.__MELFORE_KONVA_TIMELINE_DEBUG__) {
        return;
    }
    logger("debug", component, message);
};
exports.logDebug = logDebug;
/**
 * Logs message for error level and component
 * @param component the component subject of the log
 * @param message the message of the log
 */
const logError = (component, message) => logger("error", component, message);
exports.logError = logError;
/**
 * Logs message for warn level and component
 * @param component the component subject of the log
 * @param message the message of the log
 */
const logWarn = (component, message) => logger("warn", component, message);
exports.logWarn = logWarn;
