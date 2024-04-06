import { useEffect, useState } from 'react';

type Props = {
    url: string;
};

const useSSE = <T>({ url }: Props) => {
    const [isConnected, setIsConnected] = useState<boolean>(false);
    const [data, setData] = useState<T | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const eventSource = new EventSource(url);

        eventSource.onopen = () => {
            setIsConnected(true);
        };

        eventSource.onmessage = (event) => {
            const stream: T = JSON.parse(event?.data);
            setData(stream);
        };

        eventSource.onerror = () => {
            setData(null);
            setError('Error connecting to server');
        };

        return () => {
            eventSource.close();
            setIsConnected(false);
            setData(null);
            setError(null);
        };
    }, [url]);

    return { data, error, isConnected };
};

export default useSSE;
