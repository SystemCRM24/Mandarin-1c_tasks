export type LogLevel = "debug" | "error" | "warn";
/**
 * Logs message for info level and component only if debug mode enabled
 * @param component the component subject of the log
 * @param message the message of the log
 */
export declare const logDebug: (component: string, message: string) => void;
/**
 * Logs message for error level and component
 * @param component the component subject of the log
 * @param message the message of the log
 */
export declare const logError: (component: string, message: string) => void;
/**
 * Logs message for warn level and component
 * @param component the component subject of the log
 * @param message the message of the log
 */
export declare const logWarn: (component: string, message: string) => void;
