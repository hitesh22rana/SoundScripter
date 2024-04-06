import { useEffect, useRef, useState } from 'react';

import { isError } from '@/src/lib/utils';

type Props = {
    url: string;
    method: 'POST' | 'PUT' | 'PATCH';
    payload: any;
};

const useUploadWithProgress = ({ url, method, payload }: Props) => {
    const [progress, setProgress] = useState<number>(0);
    const [error, setError] = useState<string | null>(null);
    const reqRef = useRef<XMLHttpRequest | null>(null);
    const cancelUpload = useRef<() => void>();

    useEffect(() => {
        cancelUpload.current = () => {
            if (reqRef.current) {
                reqRef.current.abort();
                reqRef.current = null;
            }
            setProgress(0);
            setError('Upload cancelled');
        };
    }, []);

    useEffect(() => {
        const req = new XMLHttpRequest();
        reqRef.current = req;

        req.open(method, url);

        req.upload.addEventListener('progress', function (e) {
            const percentageUploaded = Math.floor((e.loaded / e.total) * 100);
            setProgress(percentageUploaded);
        });

        req.addEventListener('load', function () {
            const statusCode = req.status;

            if (isError(statusCode)) {
                const res = JSON.parse(req.response);
                setError(res?.detail ?? 'Something went wrong');
            }
        });

        req.addEventListener('abort', function () {
            setError('Upload cancelled');
        });

        req.send(payload);

        return () => {
            reqRef.current = null;
        };
    }, [url, method, payload]);

    return { progress, error, cancelUpload: cancelUpload.current };
};

export default useUploadWithProgress;
