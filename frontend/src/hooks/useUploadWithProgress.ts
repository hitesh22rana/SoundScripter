import { useEffect, useState } from "react";

import { isError } from "@/src/lib/utils";

type Props = {
    url: string;
    method: "POST" | "PUT" | "PATCH";
    payload: any;
};

const useUploadWithProgress = ({ url, method, payload }: Props) => {
    const [progress, setProgress] = useState<number>(0);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const req = new XMLHttpRequest();
        req.open(method, url);

        req.upload.addEventListener("progress", function (e) {
            const percentageUploaded = Math.floor((e.loaded / e.total) * 100);
            setProgress(percentageUploaded);
        });

        req.addEventListener("load", function () {
            const statusCode = req.status;

            if (isError(statusCode)) {
                setError(req.response?.detail ?? "Something went wrong");
            }
        });

        req.send(payload);

        return () => {
            setProgress(0);
            setError(null);
        };
    }, [url, method, payload]);

    return { progress, error };
};

export default useUploadWithProgress;
