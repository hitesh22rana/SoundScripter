"use client";

/*
    TODO:- Show toast on success and errors but all the notifications can be shown in the notifications list
*/

import { useCallback, useEffect, useState } from "react";
import Image from "next/image";
import { toast } from "sonner";
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/src/components/ui/popover";
import { Button } from "@/src/components/ui/button";

import useSSE from "@/src/hooks/useSSE";
import useFileStore from "@/src/store/file";
import useTranscriptionStore from "@/src/store/transcription";
import { NotificationType, Status, Task } from "@/src/types/core";

type Notification = {
    id: string;
    status: Status;
    type: NotificationType;
    task: Task;
    message: string;
    completed_at: string | null;
};

type Notificationsdata = {
    selected: string;
    data: Notification[];
};

const Notifications = () => {
    const { isConnected, data, error } = useSSE<Notification>({
        url: "http://127.0.0.1:8000/api/v1/sse/notifications",
    });

    const { updateFilesDataProgress } = useFileStore();
    const { updateTranscribeDataProgress } = useTranscriptionStore();

    const [allNotifications, setAllNotifications] = useState<Notification[]>(
        [] as Notification[]
    );

    const [notifications, setNotifications] = useState<Notificationsdata>(
        {} as Notificationsdata
    );

    useEffect(() => {
        if (!data) return;

        setAllNotifications((prev) => [...prev, data]);

        switch (data.task) {
            case "CONVERSION":
                updateFilesDataProgress(
                    data.id,
                    data.status,
                    data.completed_at
                );
                break;
            case "OPTIMIZATION":
                updateFilesDataProgress(
                    data.id,
                    data.status,
                    data.completed_at
                );
                break;
            case "TRANSCRIPTION":
                updateTranscribeDataProgress(
                    data.id,
                    data.status,
                    data.completed_at
                );
                break;
        }
    }, [data, updateFilesDataProgress, updateTranscribeDataProgress]);

    const extractNotifications = useCallback(
        (selected: string, tasks: Task[]) => {
            setNotifications({
                selected: selected,
                data: allNotifications.filter((notification) =>
                    tasks.includes(notification.task)
                ),
            });
        },
        [allNotifications]
    );

    if (!isConnected && !error) {
        return <span className="notification-loader" />;
    }

    if (error) {
        toast.error("Error", {
            description: "Notification service unavailable",
        });
        return null;
    }

    return (
        <Popover
            onOpenChange={() =>
                extractNotifications("files", ["CONVERSION", "OPTIMIZATION"])
            }
        >
            <PopoverTrigger className="relative w-8 h-8 rounded-full p-0 border-2 bg-gray-200">
                <Image
                    src="/icons/notifications.png"
                    width="20"
                    height="20"
                    alt="notifications"
                    draggable={false}
                    quality={100}
                    className="mx-auto"
                />
                {allNotifications.length > 0 ? (
                    <div className="absolute w-2 h-2 top-0 right-0 bg-red-500 rounded-full" />
                ) : null}
            </PopoverTrigger>

            <PopoverContent className="flex flex-col border mr-2 p-1 bg-gray-100">
                <div className="flex flex-row items-center justify-start border-b-2">
                    <Button
                        variant="link"
                        className={`text-black text-base font-medium hover:no-underline hover:opacity-75 rounded-none py-0 -mb-[2px] ${
                            notifications.selected === "files"
                                ? "border-b-2 border-black"
                                : "border-b-0 mb-0"
                        }`}
                        onClick={() =>
                            extractNotifications("files", [
                                "CONVERSION",
                                "OPTIMIZATION",
                            ])
                        }
                    >
                        Files
                    </Button>
                    <Button
                        variant="link"
                        className={`text-black text-base font-medium hover:no-underline hover:opacity-75 rounded-none py-0 -mb-[2px] ${
                            notifications.selected === "transcriptions"
                                ? "border-b-2 border-black"
                                : "border-b-0 mb-0"
                        }`}
                        onClick={() =>
                            extractNotifications("transcriptions", [
                                "TRANSCRIPTION",
                            ])
                        }
                    >
                        Transcriptions
                    </Button>
                </div>

                <div className="flex flex-col">
                    {notifications?.data?.length > 0 ? (
                        notifications.data.map((notification: Notification) => {
                            let fontColor;
                            let image;
                            switch (notification.type) {
                                case "SUCCESS": {
                                    fontColor = "text-green-400";
                                    image = "/icons/success.png";
                                    break;
                                }
                                case "INFO": {
                                    fontColor = "text-yellow-400";
                                    image = "/icons/info.png";
                                    break;
                                }
                                case "ERROR": {
                                    fontColor = "text-red-400";
                                    image = "/icons/error.png";
                                    break;
                                }
                            }

                            return (
                                <div
                                    key={notification.id}
                                    className={`flex flex-row items-center justify-start p-2 gap-4 rounded rounded-b-none border-b h-14`}
                                >
                                    <Image
                                        src={image}
                                        width="25"
                                        height="25"
                                        alt={notification.type}
                                    />
                                    <span className={`text-sm ${fontColor}`}>
                                        {notification.message}
                                    </span>
                                </div>
                            );
                        })
                    ) : (
                        <div className="flex flex-col items-center justify-between gap-2 my-4">
                            <Image
                                src="/images/no-notifications.jpg"
                                width="120"
                                height="120"
                                alt="no-notifications"
                                draggable={false}
                                quality={100}
                                className="mx-auto rounded-full bg-contain"
                            />
                            <span className="text-lg font-medium">
                                You are all caught up! 🎉
                            </span>
                        </div>
                    )}
                </div>
            </PopoverContent>
        </Popover>
    );
};

export default Notifications;
