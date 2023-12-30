"use client";

import { Fragment } from "react";
import useBackgroundProgressStore from "@/src/store/background-progress";

const BackgroundProgressTracker = () => {
    const { progressTracker } = useBackgroundProgressStore((state) => ({
        progressTracker: state.progressTracker,
    }));

    if (!progressTracker || progressTracker.length == 0) {
        return null;
    }

    return (
        <div className="fixed left-1/2 right-1/2 -translate-x-1/2 bottom-0 max-w-lg w-full h-40 rounded-t-2xl bg-gray-100 border shadow flex flex-col gap-4 px-5 py-4">
            <h3 className="font-medium text-lg">Uploading 1 item</h3>

            <div className="flex flex-col items-start gap-2">
                {progressTracker.map((backgroundProgress, index) => {
                    return (
                        <Fragment key={index}>{backgroundProgress}</Fragment>
                    );
                })}
            </div>
        </div>
    );
};

export default BackgroundProgressTracker;
