import React from "react";
interface SummaryHeaderProps {
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
    id: string;
}
export declare const SummaryHeaderDocs: ({ index, isLast, id }: SummaryHeaderProps) => React.JSX.Element;
declare const _default: React.MemoExoticComponent<({ index, isLast, id }: SummaryHeaderProps) => React.JSX.Element>;
export default _default;
