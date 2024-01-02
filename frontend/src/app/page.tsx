"use client";

import { useState } from "react";

import TranscriptionsList from "@/src/components/dashboard/TranscriptionsList";
import FilesList from "@/src/components/dashboard/FilesList";
import { Button } from "@/src/components/ui/button";

const list = {
    files: FilesList,
    transcriptions: TranscriptionsList,
};

export default function Page() {
    const [listType, setListType] = useState<"files" | "transcriptions">(
        "files"
    );
    const List = list[listType];

    return (
        <section className="flex flex-col items-start justify-start px-2 w-full max-w-7xl mx-auto py-10">
            <div className="flex flex-row items-center justify-center bg-gray-50 shadow mx-auto rounded-md">
                <Button
                    variant={listType === "files" ? "default" : "ghost"}
                    className="h-8 w-36 font-medium rounded-none rounded-l-md"
                    onClick={() => setListType("files")}
                >
                    Files
                </Button>
                <Button
                    variant={
                        listType === "transcriptions" ? "default" : "ghost"
                    }
                    className="h-8 w-36 font-medium rounded-none rounded-r-md"
                    onClick={() => setListType("transcriptions")}
                >
                    Transcriptions
                </Button>
            </div>

            <List />
        </section>
    );
}
