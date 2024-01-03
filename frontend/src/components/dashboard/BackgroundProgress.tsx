"use client";

import { toast } from "sonner";

import useUploadWithProgress from "@/src/hooks/useUploadWithProgress";
import useBackgroundProgressStore from "@/src/store/background-progress";
import {
    Circle,
    CircularProgress,
} from "@/src/components/ui/circular-progress";

type Props = {
    id: number;
    url: string;
    method: "POST" | "PUT" | "PATCH";
    fileName: string;
    payload: any;
};

const BackgroundProgress = ({ id, url, method, fileName, payload }: Props) => {
    const { progress, error } = useUploadWithProgress({
        url: url,
        method: method,
        payload: payload,
    });

    const { removeFromProgressTracker } = useBackgroundProgressStore(
        (state) => ({
            removeFromProgressTracker: state.removeFromProgressTracker,
        })
    );

    if (error) {
        toast.error("Error", {
            description: error,
        });
        removeFromProgressTracker(id);
        return null;
    }

    const isCompleted: boolean = progress === 100;

    if (isCompleted) {
        removeFromProgressTracker(id);
        return null;
    }

    return (
        <div className="flex flex-row items-center justify-between w-full bg-b">
            <span className="max-w-[90%] w-full text-ellipsis overflow-hidden whitespace-nowrap">
                {fileName}
            </span>
            <CircularProgress
                height="35"
                width="35"
                centerOfRotation="rotate(-90 17 17)"
            >
                <Circle
                    radius={12}
                    centerX={17}
                    centerY={17}
                    fill="transparent"
                    stroke="lightgrey"
                    percentage={100}
                    strokeWidth="4px"
                />
                <Circle
                    radius={12}
                    centerX={17}
                    centerY={17}
                    fill="transparent"
                    stroke="#303030"
                    percentage={progress}
                    strokeWidth="4px"
                />
            </CircularProgress>
        </div>
    );
};

export default BackgroundProgress;
