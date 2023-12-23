"use client";

import { useEffect, useState } from "react";
import { ColumnDef } from "@tanstack/react-table";

import { ListFile } from "@/src/types/api";
import { fetchFileList } from "@/src/lib/api";
import { DataTable } from "@/src/components/ui/data-table";

const options = {
    year: "numeric",
    month: "numeric",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
};

const columns: ColumnDef<ListFile>[] = [
    {
        accessorKey: "name",
        header: "Name",
    },
    {
        accessorKey: "type",
        header: "Type",
    },
    {
        accessorKey: "status",
        header: "Status",
        cell: ({ row }) => {
            const value: string = row.getValue("status") as string;
            let color;
            switch (value) {
                case "DONE":
                    color = "bg-green-500";
                    break;
                case "ERROR":
                    color = "bg-red-500";
                    break;
                case "PROCESSING":
                    color = "bg-yellow-500";
                    break;
                case "QUEUE":
                    color = "bg-blue-500";
                    break;
            }

            return (
                <span
                    className={`${color} text-white w-full px-4 py-1 text-xs rounded-full bg-green-500`}
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
                options as any
            ) as unknown as string,
    },
    {
        accessorKey: "completed_at",
        header: "Completed At",
        cell: ({ row }) =>
            row.getValue("completed_at")
                ? (new Date(row.getValue("completed_at")).toLocaleString(
                      "en-US",
                      options as any
                  ) as unknown as string)
                : null,
    },
];

const FilesList = () => {
    const [list, setList] = useState<ListFile[]>([] as ListFile[]);

    useEffect(() => {
        (async function () {
            try {
                const data = await fetchFileList();
                setList(data);
            } catch (err) {
                console.error(err);
            }
        })();
    }, []);

    if (!list) {
        return <h1>Loading...</h1>;
    }

    return (
        <div className="container mx-auto py-10">
            <DataTable columns={columns} data={list} />
        </div>
    );
};

export default FilesList;
