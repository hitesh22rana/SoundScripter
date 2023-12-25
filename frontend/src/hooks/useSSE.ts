import { useEffect, useState } from "react";

type Props = {
    url: string;
};

const useSSE = <T>({ url }: Props) => {
    const [isConnected, setIsConnected] = useState<boolean>(false);
    const [data, setData] = useState<T[]>([] as T[]);

    useEffect(() => {
        const eventSource = new EventSource(url);

        eventSource.onopen = () => {
            setIsConnected(true);
        };

        eventSource.onmessage = (event) => {
            let stream;
            try {
                stream = JSON.parse(event.data);
            } catch (error) {}

            console.log(stream);
        };

        return () => {
            eventSource.close();
            setIsConnected(false);
        };
    }, [url]);

    return { data };
};

export default useSSE;
