"use client";

import { useEffect } from "react";
import Image from "next/image";
import { toast } from "sonner";
import { ColumnDef } from "@tanstack/react-table";
import { ArrowUpDown, MoreHorizontal } from "lucide-react";
import { Button } from "@/src/components/ui/button";
import { DataTable } from "@/src/components/ui/data-table";
import FileUploadModal from "@/src/components/dashboard/FileUploadModal";
import TranscribeFileModal from "@/src/components/dashboard/TranscribeFileModal";
import Loader from "@/src/components/ui/loader";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/src/components/ui/dropdown-menu";

import useFileStore from "@/src/store/file";
import useModalStore from "@/src/store/modal";
import { Media, Status } from "@/src/types/core";
import { ListFileApiResponse } from "@/src/types/api";
import { dateFormatOptions, cn } from "@/src/lib/utils";

const FilesList = () => {
    const { mountModal } = useModalStore();

    const { fetchFiles, data, error, deleteFile } = useFileStore((state) => ({
        fetchFiles: state.fetchFiles,
        deleteFile: state.deleteFile,
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

    async function handleFileDelete(id: string) {
        try {
            await deleteFile(id, false);

            toast.success("Success", {
                description: "File deleted successfully",
            });
        } catch (error) {
            toast.error("Error", { description: "Failed to delete file" });
        }
    }

    const columns: ColumnDef<ListFileApiResponse>[] = [
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
                        icon = "audio.png";
                        break;
                    case "VIDEO":
                        icon = "video.png";
                        text = "Video";
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
                        Uploaded at
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
                const file: ListFileApiResponse = row.original;

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
                            >
                                <Image
                                    src="/icons/transcription.svg"
                                    width="15"
                                    height="15"
                                    alt="transcribe"
                                />
                                Transcribe
                            </DropdownMenuItem>

                            <DropdownMenuSeparator />
                            <DropdownMenuItem
                                className="cursor-pointer gap-2"
                                onClick={() => handleFileDelete(file.id)}
                            >
                                <Image
                                    src="/icons/delete.png"
                                    width="15"
                                    height="15"
                                    alt="delete"
                                />
                                Delete
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                );
            },
        },
    ];

    return (
        <div className="flex flex-col w-full px-4 pt-10 gap-5">
            <Button
                variant="default"
                className="flex flex-row items-center border-2 gap-2 w-auto md:ml-auto md:mr-0 mx-auto md:text-sm text-xs md:p-4 p-3"
                onClick={() => mountModal(<FileUploadModal />)}
            >
                <Image
                    src="/icons/upload.svg"
                    alt="Upload"
                    width={16}
                    height={16}
                    className="text-white w-4 h-4"
                />
                Upload
            </Button>
            <DataTable columns={columns} data={data} />
        </div>
    );
};

export default FilesList;
