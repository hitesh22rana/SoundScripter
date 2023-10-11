"use client";

import Image from "next/image";
import { useState } from "react";

import { FileUploader } from "react-drag-drop-files";

import { Button } from "@/src/components/ui/button";

export default function FileUpload({
    fileTypes,
}: {
    fileTypes: Array<string>;
}) {
    const [file, setFile] = useState(null);

    const handleChange = (file: any) => {
        console.log(file?.name);
        // setFile(file);
    };

    return (
        <div className="flex flex-col items-center bg-white w-full h-full py-10 rounded gap-10 shadow">
            <div className="flex flex-col items-center justify-center gap-4">
                <h3 className="text-2xl font-bold text-gray-950">
                    Upload Files
                </h3>
                <h4 className="text-gray-600">
                    Please upload the audio/video files that you would like to
                    transcribe.
                </h4>
            </div>
            <FileUploader
                handleChange={handleChange}
                name="file"
                types={fileTypes}
                classes="upload-area"
            >
                <div className="flex flex-col items-center justify-center w-full h-full outline-dashed outline-2 outline-gray-400 rounded px-5 py-10 md:mx-20 mx-10 bg-gray-50 gap-5">
                    <Image
                        src="/icons/upload-dnd.svg"
                        alt="upload-dnd"
                        width={60}
                        height={60}
                    />
                    <span className="text-gray-950 font-semibold">
                        Drag and Drop to upload files, or
                    </span>

                    <Button
                        variant="outline"
                        className="px-8 py-5 border-2 font-medium"
                    >
                        Browse files
                    </Button>

                    <span className="text-gray-500">
                        Supported formats: wav, mp3, mp4, mkv
                    </span>
                </div>
            </FileUploader>
        </div>
    );
}
