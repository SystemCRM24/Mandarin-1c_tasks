type RGBType = {
    r: number;
    g: number;
    b: number;
};
export declare const DEFAULT_ROW_LIGHT_MODE = "#F0F0F0";
export declare const ALTERNATIVE_ROW = "transparent";
export declare const DEFAULT_ROW_DARK_MODE = "#A8A8A8";
export declare const DEFAULT_STROKE_LIGHT_MODE = "grey";
export declare const DEFAULT_STROKE_DARK_MODE = "white";
export declare const getRGB: (hex: string) => {
    r: number;
    g: number;
    b: number;
};
export declare const getRGBA: (hex: string) => {
    r: number;
    g: number;
    b: number;
    a: number;
} | {
    r: number;
    g: number;
    b: number;
    a?: undefined;
};
/**
 * Gets the black / white contrast color for given color
 * @param hex the color to be contrasted in hex format (e.g. '#000000')
 */
export declare const getContrastColor: (hex: string) => "#000000" | "#FFFFFF";
export declare const RGBFromRGBA: (opacity: number, rgb: RGBType) => string;
export {};
