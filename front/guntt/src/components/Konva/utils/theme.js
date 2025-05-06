"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.RGBFromRGBA = exports.getContrastColor = exports.getRGBA = exports.getRGB = exports.DEFAULT_STROKE_DARK_MODE = exports.DEFAULT_STROKE_LIGHT_MODE = exports.DEFAULT_ROW_DARK_MODE = exports.ALTERNATIVE_ROW = exports.DEFAULT_ROW_LIGHT_MODE = void 0;
const HEX_BASE = 16;
const HEX_COLOR_LENGTH = 6;
const LUMA_FACTOR_R = 299;
const LUMA_FACTOR_G = 587;
const LUMA_FACTOR_B = 114;
const LUMA_FACTOR_BW = 128;
exports.DEFAULT_ROW_LIGHT_MODE = "#F0F0F0";
exports.ALTERNATIVE_ROW = "transparent";
exports.DEFAULT_ROW_DARK_MODE = "#A8A8A8";
exports.DEFAULT_STROKE_LIGHT_MODE = "grey";
exports.DEFAULT_STROKE_DARK_MODE = "white";
const getRGB = (hex) => {
    if (!hex || !hex.length) {
        throw new Error("Missing HEX color!");
    }
    let hexColor = hex;
    if (hexColor.indexOf("#") === 0) {
        hexColor = hexColor.slice(1);
    }
    if (hexColor.length === HEX_COLOR_LENGTH / 2) {
        hexColor = `${hexColor[0]}${hexColor[0]}${hexColor[1]}${hexColor[1]}${hexColor[2]}${hexColor[2]}`;
    }
    if (hexColor.length !== HEX_COLOR_LENGTH) {
        throw new Error("Invalid HEX color!");
    }
    const r = parseInt(hexColor.substring(0, 2), HEX_BASE);
    const g = parseInt(hexColor.substring(2, 4), HEX_BASE);
    const b = parseInt(hexColor.substring(4, 6), HEX_BASE);
    return { r: r, g: g, b: b };
};
exports.getRGB = getRGB;
const getRGBA = (hex) => {
    if (!hex || !hex.length) {
        throw new Error("Missing HEX color!");
    }
    let hexColor = hex;
    if (hexColor.indexOf("#") === 0) {
        hexColor = hexColor.slice(1);
    }
    if (hexColor.length === HEX_COLOR_LENGTH / 2) {
        hexColor = `${hexColor[0]}${hexColor[0]}${hexColor[1]}${hexColor[1]}${hexColor[2]}${hexColor[2]}`;
    }
    if (hexColor.length === HEX_COLOR_LENGTH + 2) {
        const r = parseInt(hexColor.substring(0, 2), HEX_BASE);
        const g = parseInt(hexColor.substring(2, 4), HEX_BASE);
        const b = parseInt(hexColor.substring(4, 6), HEX_BASE);
        const a = parseInt(hexColor.substring(6, 8)) / 100;
        return { r: r, g: g, b: b, a: a };
    }
    if (hexColor.length !== HEX_COLOR_LENGTH) {
        throw new Error("Invalid HEX color!");
    }
    const r = parseInt(hexColor.substring(0, 2), HEX_BASE);
    const g = parseInt(hexColor.substring(2, 4), HEX_BASE);
    const b = parseInt(hexColor.substring(4, 6), HEX_BASE);
    return { r: r, g: g, b: b };
};
exports.getRGBA = getRGBA;
/**
 * Gets the black / white contrast color for given color
 * @param hex the color to be contrasted in hex format (e.g. '#000000')
 */
const getContrastColor = (hex) => {
    const rgb = (0, exports.getRGB)(hex);
    const luma = (rgb.r * LUMA_FACTOR_R + rgb.g * LUMA_FACTOR_G + rgb.b * LUMA_FACTOR_B) / 1000;
    return luma >= LUMA_FACTOR_BW ? "#000000" : "#FFFFFF";
};
exports.getContrastColor = getContrastColor;
const RGBFromRGBA = (opacity, rgb) => {
    const r3 = Math.round((1 - opacity) * 255 + opacity * rgb.r);
    const g3 = Math.round((1 - opacity) * 255 + opacity * rgb.g);
    const b3 = Math.round((1 - opacity) * 255 + opacity * rgb.b);
    return "rgb(" + r3 + "," + g3 + "," + b3 + ")";
};
exports.RGBFromRGBA = RGBFromRGBA;
