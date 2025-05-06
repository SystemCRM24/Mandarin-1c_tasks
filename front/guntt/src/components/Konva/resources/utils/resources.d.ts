export interface Resource {
    /**
     * Unique identifier of the resource
     */
    id: string;
    /**
     * Label of the resource
     */
    label: string;
    /**
     * Color assigned to the resource, accept only HEX
     */
    color: string;
    /**
     * Color assigned to the resource for incomplete part of Task, accept only HEX
     */
    toCompleteColor?: string;
}
export declare const RESOURCE_HEADER_WIDTH = 200;
export declare const RESOURCE_TEXT_OFFSET = 12;
/**
 * Adds header resource to incoming list of resources
 * @param resources the list of all resources
 */
export declare const addHeaderResource: (resources: Resource[], headerLabel?: string) => Resource[];
/**
 * Finds resource index given a y coordinate. Used when determining the resource from pointer position.
 * Excludes the header resource, hence resources are considered index 1 based.
 * @param coordinate the y coordinate from pointer position
 * @param rowHeight the current height of rows
 * @param resources the list of all resources
 * @throws if resources is empty
 */
export declare const findResourceIndexByCoordinate: (coordinate: number, rowHeight: number, resources: Resource[]) => number;
/**
 * Finds resource object given a y coordinate. Used when determining the resource from pointer position.
 * Excludes the header resource, hence resources are considered index 1 based.
 * @param coordinate the y coordinate from pointer position
 * @param rowHeight the current height of rows
 * @param resources the list of all resources
 */
export declare const findResourceByCoordinate: (coordinate: number, rowHeight: number, resources: Resource[]) => Resource;
