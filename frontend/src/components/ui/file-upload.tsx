"use client";

import { useState } from "react";

import { FileUploader } from "react-drag-drop-files";

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
        <div className="flex flex-col items-center bg-white w-full h-full p-2 rounded">
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
            >
                <div>here</div>
            </FileUploader>
            <p className="text-gray-600"></p>
        </div>
    );
}
