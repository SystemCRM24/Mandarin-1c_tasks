"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.KonvaTimeline = exports.RESOLUTIONS = void 0;
var time_resolution_1 = require("./utils/time-resolution");
Object.defineProperty(exports, "RESOLUTIONS", { enumerable: true, get: function () { return time_resolution_1.RESOLUTIONS; } });
var KonvaTimeline_1 = require("./KonvaTimeline");
Object.defineProperty(exports, "KonvaTimeline", { enumerable: true, get: function () { return __importDefault(KonvaTimeline_1).default; } });
