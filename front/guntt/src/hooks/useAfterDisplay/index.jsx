import { useEffect, useRef } from "react";


const useAfterDisplay = (tag, isLoading, callback) => {
    const observerRef = useRef(null);
  
    useEffect(
        () => {
            if (!isLoading) {
                const targetNode = document.getElementById(tag);
                if (targetNode) {
                    const observer = new MutationObserver(
                        (mutationsList) => {
                            for (let mutation of mutationsList) {
                                if (mutation.type === 'childList') {
                                    callback();
                                    observer.disconnect();
                                    break;
                                }
                            }
                        }
                    );
                    observer.observe(targetNode, { childList: true, subtree: true });
                    observerRef.current = observer;
                }
            }
            return () => {
                if (observerRef.current) {
                    observerRef.current.disconnect();
                }
            };
        }, 
        [isLoading, callback]
    );
};

export default useAfterDisplay;