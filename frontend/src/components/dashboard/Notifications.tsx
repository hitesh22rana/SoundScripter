"use client";

import useSSE from "@/src/hooks/useSSE";
import { Status } from "@/src/types/core";

type Notification = {
    id: string;
    process: string;
    status: Status;
};

const Notifications = () => {
    const { data } = useSSE<Notification>({
        url: "http://127.0.0.1:8000/api/v1/sse/notifications",
    });

    return (
        <div>
            <h1>Notifications</h1>
            <ul>
                {data?.map((notification) => (
                    <li key={notification.id}>{notification.process}</li>
                ))}
            </ul>
        </div>
    );
};

export default Notifications;
