"use client";

import { useState } from "react";
import Image from "next/image";

import TranscriptionsList from "@/src/components/dashboard/TranscriptionsList";
import FilesList from "@/src/components/dashboard/FilesList";

import { Button } from "@/src/components/ui/button";
import useModalStore from "@/srcstore/modal";

const list = {
    files: FilesList,
    transcriptions: TranscriptionsList,
};

export default function Page() {
    const { toggleModal } = useModalStore();
    const [listType, setListType] = useState<"files" | "transcriptions">(
        "files"
    );
    const List = list[listType];

    return (
        <section className="flex flex-col items-start justify-start p-2 w-full">
            <div className="flex items-center justify-end w-full p-2">
                <Button
                    variant="default"
                    className="p-5 border-2 font-medium gap-2 mx-auto md:mx-0"
                    onClick={toggleModal}
                >
                    <Image
                        src="/icons/upload.svg"
                        alt="Upload"
                        width={20}
                        height={20}
                    />
                    Upload File
                </Button>
            </div>

            <div className="flex flex-row items-center justify-center bg-gray-50 shadow border border-gray-100 mx-auto">
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
