"use client";

import { useEffect } from "react";
import Image from "next/image";
import { ColumnDef } from "@tanstack/react-table";
import { ArrowUpDown, MoreHorizontal } from "lucide-react";
import { Button } from "@/src/components/ui/button";
import { DataTable } from "@/src/components/ui/data-table";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/src/components/ui/dropdown-menu";

import useTranscriptionStore from "@/src/store/transcription";
import { ListTranscriptionApiResponse } from "@/src/types/api";
import { Media, Status } from "@/src/types/core";
import { cn, dateFormatOptions } from "@/src/lib/utils";

const TranscriptionsList = () => {
    const {
        fetchTranscriptions,
        data,
        error: transcriptionError,
    } = useTranscriptionStore();

    useEffect(() => {
        (async function () {
            await fetchTranscriptions();
        })();
    }, [fetchTranscriptions]);

    const columns: ColumnDef<ListTranscriptionApiResponse>[] = [
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
        },
        {
            accessorKey: "type",
            header: () => {
                return (
                    <span className="font-medium md:text-base text-sm text-black">
                        Type
                    </span>
                );
            },
            cell: ({ row }) => {
                const value: Media = row.getValue("type") as Media;
                let icon;
                switch (value) {
                    case "AUDIO":
                        icon = "audio.png";
                        break;
                    case "VIDEO":
                        icon = "video.png";
                        break;
                }

                return (
                    <div className="flex flex-row gap-2">
                        <Image
                            src={`/icons/${icon}`}
                            width="20"
                            height="20"
                            alt={icon}
                        />
                        <span>{value}</span>
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
            cell: ({ row }) =>
                new Date(row.getValue("created_at")).toLocaleString(
                    "en-US",
                    dateFormatOptions as any
                ) as unknown as string,
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
            cell: ({ row }) =>
                row.getValue("completed_at")
                    ? (new Date(row.getValue("completed_at")).toLocaleString(
                          "en-US",
                          dateFormatOptions as any
                      ) as unknown as string)
                    : null,
        },
        {
            id: "actions",
            cell: ({ row }) => {
                return (
                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <Button variant="ghost" className="h-6 w-6 p-0">
                                <span className="sr-only">Open menu</span>
                                <MoreHorizontal className="h-4 w-4" />
                            </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                            <DropdownMenuItem className="cursor-pointer gap-2">
                                <Image
                                    src="/icons/download.png"
                                    width="15"
                                    height="15"
                                    alt="transcribe"
                                />
                                Download
                            </DropdownMenuItem>

                            <DropdownMenuSeparator />
                            <DropdownMenuItem className="cursor-pointer gap-2">
                                <Image
                                    src="/icons/terminate.png"
                                    width="15"
                                    height="15"
                                    alt="delete"
                                />
                                Terminate
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                );
            },
        },
    ];

    if (transcriptionError) {
        return (
            <div className="flex justify-center items-center w-full h-40">
                <span className="text-red-500">{transcriptionError}</span>
            </div>
        );
    }

    if (!data) {
        return (
            <div className="flex justify-center items-center w-full h-40">
                <span className="loader" />
            </div>
        );
    }

    return (
        <div className="w-full mx-auto px-4 pt-10">
            <DataTable columns={columns} data={data} />
        </div>
    );
};

export default TranscriptionsList;
