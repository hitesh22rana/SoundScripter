"use client";

import { useEffect, useState } from "react";
import { ColumnDef } from "@tanstack/react-table";
import { toast } from "sonner";
import {
    ArrowUpDown,
    Download,
    BadgeX,
    MoreHorizontal,
    FileAudio2,
    FileVideo2,
} from "lucide-react";
import { Button } from "@/src/components/ui/button";
import { DataTable } from "@/src/components/ui/data-table";
import TranscriptionTerminateModal from "@/src/components/dashboard/modals/TranscriptionTerminateModal";
import Loader from "@/src/components/ui/loader";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/src/components/ui/dropdown-menu";

import useModalStore from "@/src/store/modal";
import useTranscriptionStore from "@/src/store/transcription";
import { TranscriptionApiResponse } from "@/src/types/api";
import { Media, Status } from "@/src/types/core";
import { cn, dateFormatOptions } from "@/src/lib/utils";

const TranscriptionsList = () => {
    const { mountModal } = useModalStore();

    const { fetchTranscriptions, data, downloadTranscription } =
        useTranscriptionStore((state) => ({
            fetchTranscriptions: state.fetchTranscriptions,
            data: state.data,
            downloadTranscription: state.downloadTranscription,
        }));

    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        (async function () {
            try {
                await fetchTranscriptions();
            } catch (error: any) {
                setError(error?.message || "Failed to fetch files data");
            }
        })();
    }, [fetchTranscriptions]);

    if (error) {
        return (
            <div className="flex justify-center items-center w-full h-40">
                <span className="text-red-500">{error}</span>
            </div>
        );
    }

    if (!data) {
        return <Loader />;
    }

    async function download(id: string, fileName: string) {
        try {
            await downloadTranscription(id, fileName);

            toast.success("Success", {
                description: "File download successfully",
            });
        } catch (error: any) {
            toast.error("Error", {
                description:
                    error?.message || "Failed to download transcription",
            });
        }
    }

    const columns: ColumnDef<TranscriptionApiResponse>[] = [
        {
            accessorKey: "name",
            header: ({ column }) => {
                return (
                    <Button
                        variant="ghost"
                        onClick={() =>
                            column.toggleSorting(column.getIsSorted() === "asc")
                        }
                        className="px-0 font-medium text-base text-black hover:text-gray-600"
                    >
                        File name
                        <ArrowUpDown className="ml-2 h-4 w-4" />
                    </Button>
                );
            },
            cell: ({ row }) => {
                return (
                    <span className="line-clamp-1">{row.getValue("name")}</span>
                );
            },
        },
        {
            accessorKey: "type",
            header: () => {
                return (
                    <span className="font-medium md:text-base text-sm text-black">
                        Media Type
                    </span>
                );
            },
            cell: ({ row }) => {
                const value: Media = row.getValue("type") as Media;
                let icon;
                let text;
                switch (value) {
                    case "AUDIO":
                        text = "Audio";
                        icon = <FileAudio2 className="h-5 w-5" />;
                        break;
                    case "VIDEO":
                        text = "Video";
                        icon = <FileVideo2 className="h-5 w-5" />;
                        break;
                }

                return (
                    <div className="flex flex-row gap-2 line-clamp-1">
                        {icon}
                        <span>{text}</span>
                    </div>
                );
            },
        },
        {
            accessorKey: "status",
            header: () => {
                return (
                    <span className="font-medium md:text-base text-sm text-black">
                        Status
                    </span>
                );
            },
            cell: ({ row }) => {
                const value: Status = row.getValue("status") as Status;
                let backgroundColor;
                let fontColor;
                let text;
                switch (value) {
                    case "DONE":
                        backgroundColor = "bg-green-100";
                        fontColor = "text-green-600";
                        text = "Done";
                        break;
                    case "ERROR":
                        backgroundColor = "bg-red-100";
                        fontColor = "text-red-600";
                        text = "Error";
                        break;
                    case "PROCESSING":
                        backgroundColor = "bg-blue-100";
                        fontColor = "text-blue-600";
                        text = "Processing";
                        break;
                    case "QUEUE":
                        backgroundColor = "bg-yellow-100";
                        fontColor = "text-yellow-600";
                        text = "Queued";
                        break;
                }

                return (
                    <span
                        className={cn(
                            "py-1 px-4 text-center md:text-sm text-xs font-medium rounded-md",
                            backgroundColor,
                            fontColor
                        )}
                    >
                        {text}
                    </span>
                );
            },
        },
        {
            accessorKey: "created_at",
            header: ({ column }) => {
                return (
                    <Button
                        variant="ghost"
                        onClick={() =>
                            column.toggleSorting(column.getIsSorted() === "asc")
                        }
                        className="px-0 font-medium text-base text-black hover:text-gray-600"
                    >
                        Started at
                        <ArrowUpDown className="ml-2 h-4 w-4" />
                    </Button>
                );
            },
            cell: ({ row }) => {
                return (
                    <span className="line-clamp-1">
                        {
                            new Date(row.getValue("created_at")).toLocaleString(
                                "en-US",
                                dateFormatOptions as any
                            ) as unknown as string
                        }
                    </span>
                );
            },
        },
        {
            accessorKey: "completed_at",
            header: ({ column }) => {
                return (
                    <Button
                        variant="ghost"
                        onClick={() =>
                            column.toggleSorting(column.getIsSorted() === "asc")
                        }
                        className="px-0 font-medium text-base text-black hover:text-gray-600"
                    >
                        Completed at
                        <ArrowUpDown className="ml-2 h-4 w-4" />
                    </Button>
                );
            },
            cell: ({ row }) => {
                return (
                    <span className="line-clamp-1">
                        {row.getValue("completed_at")
                            ? (new Date(
                                  row.getValue("completed_at")
                              ).toLocaleString(
                                  "en-US",
                                  dateFormatOptions as any
                              ) as unknown as string)
                            : null}
                    </span>
                );
            },
        },
        {
            id: "actions",
            cell: ({ row }) => {
                const transcription: TranscriptionApiResponse = row.original;
                const isCompleted = transcription.completed_at !== null;
                const isCompletedSuccessFully =
                    isCompleted && transcription.status === "DONE";

                return (
                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <Button
                                variant="outline"
                                className="h-6 w-6 p-0 focus-within:ring-0 focus-within:outline-none focus-visible:ring-0"
                            >
                                <span className="sr-only">Open menu</span>
                                <MoreHorizontal className="h-4 w-4" />
                            </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                            <DropdownMenuItem
                                className="cursor-pointer gap-2"
                                disabled={!isCompletedSuccessFully}
                                onClick={() =>
                                    download(
                                        transcription.id,
                                        transcription.name
                                    )
                                }
                            >
                                <Download className="h-4 w-4" />
                                Download
                            </DropdownMenuItem>

                            <DropdownMenuSeparator />
                            <DropdownMenuItem
                                className="cursor-pointer gap-2"
                                disabled={isCompleted}
                                onClick={() => {
                                    mountModal(
                                        <TranscriptionTerminateModal
                                            {...transcription}
                                        />
                                    );
                                }}
                            >
                                <BadgeX className="h-4 w-4" />
                                Terminate
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                );
            },
        },
    ];

    return (
        <div className="w-full mx-auto px-4 pt-10">
            <DataTable columns={columns} data={data} />
        </div>
    );
};

export default TranscriptionsList;
