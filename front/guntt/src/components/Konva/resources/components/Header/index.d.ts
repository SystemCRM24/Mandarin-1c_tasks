import React from "react";
import { Resource } from "../../utils/resources";
export interface ResourceHeaderProps {
    /**
     * The row index of current resource
     */
    index: number;
    /**
     * Flag to identify if resource is last to be shown
     */
    isLast?: boolean;
    /**
     * The resource object to handle
     */
    resource: Resource;
    /**
     * On click event
     */
    onClick?: () => void;
    /**
     * Prop that idicate if resource is header
     */
    header?: boolean;
}
export declare const ResourceHeaderDocs: ({ index, isLast, resource, header }: ResourceHeaderProps) => React.JSX.Element;
declare const _default: React.MemoExoticComponent<({ index, isLast, resource, header }: ResourceHeaderProps) => React.JSX.Element>;
export default _default;
