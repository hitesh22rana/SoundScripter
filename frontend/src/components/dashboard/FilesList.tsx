'use client';

import { useEffect, useState } from 'react';
import { ColumnDef } from '@tanstack/react-table';
import {
    ArrowUpDown,
    FileAudio2,
    FileText,
    FileVideo2,
    MoreHorizontal,
    Trash2,
    UploadCloud,
} from 'lucide-react';
import { Button } from '@/src/components/ui/button';
import { DataTable } from '@/src/components/ui/data-table';
import FileUploadModal from '@/src/components/dashboard/modals/FileUploadModal';
import TranscribeFileModal from '@/src/components/dashboard/modals/TranscribeFileModal';
import DeleteFileModal from '@/src/components/dashboard/modals/DeleteFileModal';
import Loader from '@/src/components/ui/loader';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/src/components/ui/dropdown-menu';

import useModalStore from '@/src/store/modal';
import useFileStore from '@/src/store/file';
import { Media, Status } from '@/src/types/core';
import { FileApiResponse } from '@/src/types/api';
import { dateFormatOptions, cn } from '@/src/lib/utils';

const FilesList = () => {
    const { mountModal } = useModalStore();

    const { fetchFiles, data } = useFileStore();

    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        (async function () {
            try {
                await fetchFiles();
            } catch (error: any) {
                setError(error?.message || 'Failed to fetch files data');
            }
        })();
    }, [fetchFiles]);

    if (error) {
        return (
            <div className="flex h-40 w-full items-center justify-center">
                <span className="text-red-500">{error}</span>
            </div>
        );
    }

    if (!data) {
        return <Loader />;
    }

    const columns: ColumnDef<FileApiResponse>[] = [
        {
            accessorKey: 'name',
            header: ({ column }) => {
                return (
                    <Button
                        variant="ghost"
                        onClick={() =>
                            column.toggleSorting(column.getIsSorted() === 'asc')
                        }
                        className="flex w-auto min-w-[120px] max-w-xs flex-row items-center justify-start px-0 text-base font-medium text-black hover:text-gray-600 md:w-[320px]"
                    >
                        File name
                        <ArrowUpDown className="ml-2 h-4 w-4" />
                    </Button>
                );
            },
            cell: ({ row }) => {
                return (
                    <span className="line-clamp-1 max-w-xs">
                        {row.getValue('name')}
                    </span>
                );
            },
        },
        {
            accessorKey: 'type',
            header: () => {
                return (
                    <span className="line-clamp-1 min-w-[80px] text-sm font-medium text-black md:text-base">
                        Media type
                    </span>
                );
            },
            cell: ({ row }) => {
                const value: Media = row.getValue('type') as Media;
                let icon;
                let text;
                switch (value) {
                    case 'AUDIO':
                        text = 'Audio';
                        icon = <FileAudio2 className="h-4 w-4 md:h-5 md:w-5" />;
                        break;
                    case 'VIDEO':
                        text = 'Video';
                        icon = <FileVideo2 className="h-4 w-4 md:h-5 md:w-5" />;
                        break;
                }

                return (
                    <div className="line-clamp-1 flex flex-row gap-2">
                        {icon}
                        <span>{text}</span>
                    </div>
                );
            },
        },
        {
            accessorKey: 'status',
            header: () => {
                return (
                    <span className="line-clamp-1 text-center text-sm font-medium text-black md:text-base">
                        Status
                    </span>
                );
            },
            cell: ({ row }) => {
                const value: Status = row.getValue('status') as Status;
                let backgroundColor;
                let fontColor;
                let text;
                switch (value) {
                    case 'DONE':
                        backgroundColor = 'bg-green-100';
                        fontColor = 'text-green-600';
                        text = 'Done';
                        break;
                    case 'ERROR':
                        backgroundColor = 'bg-red-100';
                        fontColor = 'text-red-600';
                        text = 'Error';
                        break;
                    case 'PROCESSING':
                        backgroundColor = 'bg-blue-100';
                        fontColor = 'text-blue-600';
                        text = 'Processing';
                        break;
                    case 'QUEUE':
                        backgroundColor = 'bg-yellow-100';
                        fontColor = 'text-yellow-600';
                        text = 'Queued';
                        break;
                }

                return (
                    <div className="mx-auto flex w-[100px] items-center justify-start">
                        <span
                            className={cn(
                                'w-full rounded-md px-2 py-1 text-center text-xs font-medium md:text-sm',
                                backgroundColor,
                                fontColor,
                            )}
                        >
                            {text}
                        </span>
                    </div>
                );
            },
        },
        {
            accessorKey: 'created_at',
            header: ({ column }) => {
                return (
                    <Button
                        variant="ghost"
                        onClick={() =>
                            column.toggleSorting(column.getIsSorted() === 'asc')
                        }
                        className="flex min-w-[120px] flex-row items-center justify-start px-0 text-base font-medium text-black hover:text-gray-600"
                    >
                        Uploaded at
                        <ArrowUpDown className="ml-2 h-4 w-4" />
                    </Button>
                );
            },
            cell: ({ row }) => {
                console.log(row.getValue('created_at'));
                return (
                    <span className="line-clamp-1">
                        {
                            new Date(row.getValue('created_at')).toLocaleString(
                                'en-US',
                                dateFormatOptions as any,
                            ) as unknown as string
                        }
                    </span>
                );
            },
        },
        {
            accessorKey: 'completed_at',
            header: ({ column }) => {
                return (
                    <Button
                        variant="ghost"
                        onClick={() =>
                            column.toggleSorting(column.getIsSorted() === 'asc')
                        }
                        className="flex min-w-[140px] flex-row items-center justify-start px-0 text-base font-medium text-black hover:text-gray-600"
                    >
                        Completed at
                        <ArrowUpDown className="ml-2 h-4 w-4" />
                    </Button>
                );
            },
            cell: ({ row }) => {
                console.log(row.getValue('completed_at'));
                return (
                    <span className="line-clamp-1">
                        {row.getValue('completed_at')
                            ? (new Date(
                                  row.getValue('completed_at'),
                              ).toLocaleString(
                                  'en-US',
                                  dateFormatOptions as any,
                              ) as unknown as string)
                            : null}
                    </span>
                );
            },
        },
        {
            accessorKey: 'time_taken',
            header: ({ column }) => {
                return (
                    <Button
                        variant="ghost"
                        onClick={() =>
                            column.toggleSorting(column.getIsSorted() === 'asc')
                        }
                        className="flex min-w-[120px] flex-row items-center justify-start px-0 text-base font-medium text-black hover:text-gray-600"
                    >
                        Time taken
                        <ArrowUpDown className="ml-2 h-4 w-4" />
                    </Button>
                );
            },
            cell: ({ row }) => {
                const timeTakenInSec: number = Math.max(
                    (Date.parse(row.getValue('completed_at')) -
                        Date.parse(row.getValue('created_at'))) /
                        1000,
                    0,
                );

                const timeTaken: string = timeTakenInSec
                    ? timeTakenInSec.toFixed(2) + 's'
                    : 'Uploading...';

                return <span className="line-clamp-1">{timeTaken}</span>;
            },
        },
        {
            id: 'actions',
            cell: ({ row }) => {
                const file: FileApiResponse = row.original;
                const isCompleted: boolean = file.completed_at !== null;
                const isCompletedSuccessFully: boolean =
                    isCompleted && file.status === 'DONE';

                return (
                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <Button
                                variant="outline"
                                className="h-5 w-5 p-0 focus-within:outline-none focus-within:ring-0 focus-visible:ring-0 md:h-6 md:w-6"
                            >
                                <span className="sr-only">Open menu</span>
                                <MoreHorizontal className="h-3 w-3 md:h-4 md:w-4" />
                            </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                            <DropdownMenuItem
                                className="cursor-pointer gap-2"
                                onClick={() =>
                                    mountModal(
                                        <TranscribeFileModal {...file} />,
                                    )
                                }
                                disabled={!isCompletedSuccessFully}
                            >
                                <FileText className="h-3 w-3 md:h-4 md:w-4" />
                                Transcribe
                            </DropdownMenuItem>

                            <DropdownMenuSeparator />
                            <DropdownMenuItem
                                className="cursor-pointer gap-2"
                                disabled={!isCompleted}
                                onClick={() =>
                                    mountModal(<DeleteFileModal {...file} />)
                                }
                            >
                                <Trash2 className="h-4 w-4" />
                                Delete
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                );
            },
        },
    ];

    return (
        <div className="flex w-full flex-col px-2 pt-5 md:px-4">
            <Button
                variant="default"
                className="mx-auto mb-5 flex w-auto flex-row items-center gap-2 px-8 py-3 text-xs md:ml-auto md:mr-0 md:px-4 md:py-4 md:text-sm"
                onClick={() => mountModal(<FileUploadModal />)}
            >
                <UploadCloud className="h-4 w-4" />
                Upload
            </Button>
            <DataTable columns={columns} data={data} />
        </div>
    );
};

export default FilesList;
