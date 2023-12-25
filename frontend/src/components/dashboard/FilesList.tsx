"use client";

import { useEffect } from "react";
import Image from "next/image";
import { toast } from "react-toastify";
import { ColumnDef } from "@tanstack/react-table";
import { MoreHorizontal } from "lucide-react";
import { Button } from "@/src/components/ui/button";
import { DataTable } from "@/src/components/ui/data-table";
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
import { ListFile } from "@/src/types/api";
import { dateFormatOptions } from "@/src/lib/utils";

const FilesList = () => {
    const { toggleModal } = useModalStore();
    const { fetchFiles, data, deleteFile, error: filesError } = useFileStore();

    useEffect(() => {
        fetchFiles();
    }, []);

    if (filesError) {
        return (
            <div className="flex justify-center items-center w-full h-40">
                <span className="text-red-500">{filesError}</span>
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

    async function handleFileDelete(id: string) {
        try {
            deleteFile(id, true);
            toast.success("File deleted successfully");
        } catch (error) {
            toast.error("Failed to delete file");
        }
    }

    const columns: ColumnDef<ListFile>[] = [
        {
            accessorKey: "name",
            header: "Name",
        },
        {
            accessorKey: "type",
            header: "Type",
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
            header: "Status",
            cell: ({ row }) => {
                const value: Status = row.getValue("status") as Status;
                let backgroundColor;
                switch (value) {
                    case "DONE":
                        backgroundColor = "bg-green-500";
                        break;
                    case "ERROR":
                        backgroundColor = "bg-red-500";
                        break;
                    case "PROCESSING":
                        backgroundColor = "bg-yellow-500";
                        break;
                    case "QUEUE":
                        backgroundColor = "bg-blue-500";
                        break;
                }

                return (
                    <span
                        className={`${backgroundColor} text-white w-full px-4 py-1 md:text-xs rounded-full`}
                    >
                        {value}
                    </span>
                );
            },
        },
        {
            accessorKey: "created_at",
            header: "Created At",
            cell: ({ row }) =>
                new Date(row.getValue("created_at")).toLocaleString(
                    "en-US",
                    dateFormatOptions as any
                ) as unknown as string,
        },
        {
            accessorKey: "completed_at",
            header: "Completed At",
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
                const file = row.original;

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
                onClick={toggleModal}
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
