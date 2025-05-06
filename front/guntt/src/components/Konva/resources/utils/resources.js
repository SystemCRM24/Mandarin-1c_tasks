"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.findResourceByCoordinate = exports.findResourceIndexByCoordinate = exports.addHeaderResource = exports.RESOURCE_TEXT_OFFSET = exports.RESOURCE_HEADER_WIDTH = void 0;
const RESOURCE_HEADER = {
    id: "-1",
    color: "transparent",
    label: "Header",
};
exports.RESOURCE_HEADER_WIDTH = 200;
exports.RESOURCE_TEXT_OFFSET = 12;
/**
 * Adds header resource to incoming list of resources
 * @param resources the list of all resources
 */
const addHeaderResource = (resources, headerLabel) => [
    Object.assign(Object.assign({}, RESOURCE_HEADER), { label: headerLabel || RESOURCE_HEADER.label }),
    ...resources,
];
exports.addHeaderResource = addHeaderResource;
/**
 * Finds resource index given a y coordinate. Used when determining the resource from pointer position.
 * Excludes the header resource, hence resources are considered index 1 based.
 * @param coordinate the y coordinate from pointer position
 * @param rowHeight the current height of rows
 * @param resources the list of all resources
 * @throws if resources is empty
 */
const findResourceIndexByCoordinate = (coordinate, rowHeight, resources) => {
    if (!resources || !resources.length) {
        // TODO#lb: improve adding KonvaTimeline error
        throw new Error("Resources is empty");
    }
    let resourceIndex = Math.floor(coordinate / rowHeight);
    if (resourceIndex < 1) {
        resourceIndex = 1;
    }
    if (resources.length <= resourceIndex) {
        resourceIndex = resources.length - 1;
    }
    return resourceIndex;
};
exports.findResourceIndexByCoordinate = findResourceIndexByCoordinate;
/**
 * Finds resource object given a y coordinate. Used when determining the resource from pointer position.
 * Excludes the header resource, hence resources are considered index 1 based.
 * @param coordinate the y coordinate from pointer position
 * @param rowHeight the current height of rows
 * @param resources the list of all resources
 */
const findResourceByCoordinate = (coordinate, rowHeight, resources) => {
    const resourceIndex = (0, exports.findResourceIndexByCoordinate)(coordinate, rowHeight, resources);
    return resources[resourceIndex];
};
exports.findResourceByCoordinate = findResourceByCoordinate;
