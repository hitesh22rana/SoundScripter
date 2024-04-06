'use client';

import { useCallback, useEffect, useState } from 'react';
import Image from 'next/image';
import { toast } from 'sonner';
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from '@/src/components/ui/popover';
import { Button } from '@/src/components/ui/button';
import { Bell, BadgeAlert, BadgeCheck, BadgeX } from 'lucide-react';

import useSSE from '@/src/hooks/useSSE';
import useFileStore from '@/src/store/file';
import useTranscriptionStore from '@/src/store/transcription';
import { NotificationType, Status, Task } from '@/src/types/core';
import { cn } from '@/src/lib/utils';

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
        url: 'http://127.0.0.1:8000/api/v1/sse/notifications',
    });

    const { updateFilesDataProgress, fetchFiles } = useFileStore();
    const { updateTranscribeDataProgress, removeTranscription } =
        useTranscriptionStore();

    const [allNotifications, setAllNotifications] = useState<Notification[]>(
        [] as Notification[],
    );

    const [notifications, setNotifications] = useState<Notificationsdata>(
        {} as Notificationsdata,
    );

    useEffect(() => {
        if (!data) return;

        setAllNotifications((prev) => [...prev, data]);

        switch (data.type) {
            case 'SUCCESS':
                toast.success('Success', {
                    description: data.message,
                });
                break;
            case 'ERROR':
                toast.error('Error', {
                    description: data.message,
                });
                break;
            case 'INFO':
                fetchFiles();
                break;
        }

        switch (data.task) {
            case 'CONVERSION':
                updateFilesDataProgress(
                    data.id,
                    data.status,
                    data.completed_at,
                );
                break;
            case 'OPTIMIZATION':
                updateFilesDataProgress(
                    data.id,
                    data.status,
                    data.completed_at,
                );
                break;
            case 'TRANSCRIPTION':
                updateTranscribeDataProgress(
                    data.id,
                    data.status,
                    data.completed_at,
                );
                break;
            case 'TERMINATE':
                removeTranscription(data.id, 'task_ids');
                break;
        }
    }, [
        data,
        fetchFiles,
        updateFilesDataProgress,
        updateTranscribeDataProgress,
        removeTranscription,
    ]);

    const extractNotifications = useCallback(
        (selected: string, tasks: Task[]) => {
            setNotifications({
                selected: selected,
                data: allNotifications.filter((notification) =>
                    tasks.includes(notification.task),
                ),
            });
        },
        [allNotifications],
    );

    if (!isConnected && !error) {
        return <span className="notification-loader" />;
    }

    if (error) {
        toast.error('Error', {
            description: 'Notification service unavailable',
        });
        return null;
    }

    return (
        <Popover
            onOpenChange={() =>
                extractNotifications('files', ['CONVERSION', 'OPTIMIZATION'])
            }
        >
            <PopoverTrigger className="relative w-8 h-8 rounded-full border shadow-sm bg-gray-50">
                <Bell className="h-5 w-5 mx-auto" />
                {allNotifications.length > 0 ? (
                    <div className="absolute w-2 h-2 top-[2px] right-[2px] bg-red-500 rounded-full" />
                ) : null}
            </PopoverTrigger>

            <PopoverContent className="flex flex-col border mr-2 bg-gray-50 max-h-80 h-full overflow-y-scroll p-1">
                <div className="flex flex-row items-center justify-start border-b-2">
                    <Button
                        variant="link"
                        className={cn(
                            'text-black text-base font-medium hover:no-underline hover:opacity-75 rounded-none py-0 -mb-[2px]',
                            notifications.selected === 'files'
                                ? 'border-b-2 border-black'
                                : 'border-b-0 mb-0',
                        )}
                        onClick={() =>
                            extractNotifications('files', [
                                'CONVERSION',
                                'OPTIMIZATION',
                            ])
                        }
                    >
                        Files
                    </Button>
                    <Button
                        variant="link"
                        className={`text-black text-base font-medium hover:no-underline hover:opacity-75 rounded-none py-0 -mb-[2px] ${
                            notifications.selected === 'transcriptions'
                                ? 'border-b-2 border-black'
                                : 'border-b-0 mb-0'
                        }`}
                        onClick={() =>
                            extractNotifications('transcriptions', [
                                'TRANSCRIPTION',
                            ])
                        }
                    >
                        Transcriptions
                    </Button>
                </div>

                <div className="flex flex-col">
                    {notifications?.data?.length > 0 ? (
                        notifications.data.map(
                            (notification: Notification, index: number) => {
                                let icon;
                                switch (notification.type) {
                                    case 'SUCCESS': {
                                        icon = (
                                            <BadgeCheck className="min-h-[24px] min-w-[24px]" />
                                        );
                                        break;
                                    }
                                    case 'INFO': {
                                        icon = (
                                            <BadgeAlert className="min-h-[24px] min-w-[24px]" />
                                        );
                                        break;
                                    }
                                    case 'ERROR': {
                                        icon = (
                                            <BadgeX className="min-h-[24px] min-w-[24px]" />
                                        );
                                        break;
                                    }
                                }

                                return (
                                    <div
                                        key={index}
                                        className="flex flex-row items-center justify-start p-2 rounded rounded-b-none border-b"
                                    >
                                        {icon}
                                        <span className="text-sm font-medium text-gray-600 line-clamp-1 ml-2">
                                            {notification.message}
                                        </span>
                                    </div>
                                );
                            },
                        )
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
