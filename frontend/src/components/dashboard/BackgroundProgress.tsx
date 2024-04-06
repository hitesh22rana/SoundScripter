'use client';

import { useEffect } from 'react';
import { toast } from 'sonner';
import { Check, FileAudio2, FileVideo2, X } from 'lucide-react';

import { cn, getFormattedDate, humanReadableSize } from '@/src/lib/utils';
import useUploadWithProgress from '@/src/hooks/useUploadWithProgress';
import useBackgroundProgressStore from '@/src/store/background-progress';
import { Media } from '@/src/types/core';

type Props = {
    id: number;
    url: string;
    method: 'POST' | 'PUT' | 'PATCH';
    fileName: string;
    fileType: Media;
    fileSize: number;
    payload: any;
};

const BackgroundProgress = ({
    id,
    url,
    method,
    fileName,
    fileType,
    fileSize,
    payload,
}: Props) => {
    const { progress, error, cancelUpload } = useUploadWithProgress({
        url: url,
        method: method,
        payload: payload,
    });
    const { removeFromProgressTracker } = useBackgroundProgressStore();
    const isCompleted: boolean = progress == 100;

    useEffect(() => {
        let timeOut: NodeJS.Timeout | null;
        if (isCompleted) {
            timeOut = setTimeout(() => {
                removeFromProgressTracker(id);
            }, 500);
        }

        return () => {
            if (timeOut) {
                clearTimeout(timeOut);
            }
        };
    }, [id, isCompleted, removeFromProgressTracker]);

    if (error) {
        toast.error('Error', {
            description: error,
        });
        removeFromProgressTracker(id);
        return;
    }

    return (
        <div
            className={cn(
                isCompleted && 'opacity-0',
                'relative flex flex-row items-center justify-between w-full bg-gray-50 p-2 border shadow rounded-md gap-4 transition-opacity delay-100 duration-200',
            )}
        >
            <div className="flex flex-row items-center justify-start gap-2 w-full">
                {fileType === 'AUDIO' ? (
                    <FileAudio2 className="md:h-8 md:w-8 h-4 w-4" />
                ) : (
                    <FileVideo2 className="md:h-8 md:w-8 h-4 w-4" />
                )}

                <div className="flex flex-col items-start justify-between w-full">
                    <span className="w-full line-clamp-1 font-semibold text-gray-900">
                        {fileName}
                    </span>

                    <span className="text-xs text-gray-500 font-medium">
                        {getFormattedDate()} - {humanReadableSize(fileSize)}
                    </span>
                </div>
            </div>
            <div className="max-w-[40%] w-full flex flex-row items-center justify-between gap-2">
                <div className="flex flex-row w-full h-1.5 rounded">
                    <span
                        className={cn(
                            'bg-green-400 rounded',
                            !isCompleted && 'rounded-r-none',
                        )}
                        style={{ width: `${progress}%` }}
                    />
                    <span
                        className={cn(
                            'bg-gray-200 rounded',
                            !isCompleted && 'rounded-l-none',
                        )}
                        style={{ width: `${100 - progress}%` }}
                    />
                </div>
                {isCompleted ? (
                    <Check className="w-6 h-6 text-green-500" />
                ) : (
                    <X
                        className="cursor-pointer w-6 h-6 text-gray-500"
                        onClick={cancelUpload}
                    />
                )}
            </div>
        </div>
    );
};

export default BackgroundProgress;
