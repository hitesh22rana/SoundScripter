"use client";

import { useEffect } from "react";
import { ColumnDef } from "@tanstack/react-table";
import {
    ArrowUpDown,
    FileAudio2,
    FileText,
    FileVideo2,
    MoreHorizontal,
    Trash2,
    UploadCloud,
} from "lucide-react";
import { Button } from "@/src/components/ui/button";
import { DataTable } from "@/src/components/ui/data-table";
import FileUploadModal from "@/src/components/dashboard/modals/FileUploadModal";
import TranscribeFileModal from "@/src/components/dashboard/modals/TranscribeFileModal";
import DeleteFileModal from "@/src/components/dashboard/modals/DeleteFileModal";
import Loader from "@/src/components/ui/loader";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/src/components/ui/dropdown-menu";

import useModalStore from "@/src/store/modal";
import useFileStore from "@/src/store/file";
import { Media, Status } from "@/src/types/core";
import { FileApiResponse } from "@/src/types/api";
import { dateFormatOptions, cn } from "@/src/lib/utils";

const FilesList = () => {
    const { mountModal } = useModalStore();

    const { fetchFiles, data, error } = useFileStore((state) => ({
        fetchFiles: state.fetchFiles,
        data: state.data,
        error: state.error,
    }));

    useEffect(() => {
        fetchFiles();
    }, [fetchFiles]);

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

    const columns: ColumnDef<FileApiResponse>[] = [
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
                    <span className="font-medium md:text-base text-sm text-black line-clamp-1">
                        Media type
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
                    <span className="font-medium md:text-base text-cente text-sm text-black">
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
                        Uploaded at
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
                const file: FileApiResponse = row.original;
                const isCompleted: boolean = file.completed_at !== null;
                const isCompletedSuccessFully: boolean =
                    isCompleted && file.status === "DONE";

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
                                onClick={() =>
                                    mountModal(
                                        <TranscribeFileModal {...file} />
                                    )
                                }
                                disabled={!isCompletedSuccessFully}
                            >
                                <FileText className="h-4 w-4" />
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
        <div className="flex flex-col w-full px-4 pt-10">
            <Button
                variant="default"
                className="flex flex-row items-center gap-2 w-auto md:ml-auto md:mr-0 mx-auto md:text-sm text-xs md:p-4 p-3 mb-5"
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
