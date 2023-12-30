"use client";

import useUploadWithProgress from "@/src/hooks/useUploadWithProgress";

type Props = {
    url: string;
    method: "POST" | "PUT" | "PATCH";
    fileName: string;
    payload: any;
};

const BackgroundProgress = ({ url, method, fileName, payload }: Props) => {
    const { progress, error } = useUploadWithProgress({
        url: url,
        method: method,
        payload: payload,
    });

    return (
        <div className="flex flex-row items-center justify-between w-full">
            <span>{fileName}</span>
            <span>{progress}</span>
        </div>
    );
};

export default BackgroundProgress;
