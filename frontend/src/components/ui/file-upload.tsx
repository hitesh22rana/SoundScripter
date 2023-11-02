"use client";

import Image from "next/image";
import { Fragment, useState } from "react";

import Dropzone, { Accept } from "react-dropzone";

import { Button } from "@/src/components/ui/button";

export default function FileUpload({ fileTypes }: { fileTypes: Accept }) {
    const [files, setFiles] = useState<Array<File>>([]);

    console.log(files);

    return (
        <Fragment>
            <div className="flex flex-col items-center bg-white w-full h-full py-10 rounded gap-10 shadow px-5">
                <div className="flex flex-col items-center justify-center gap-4">
                    <h3 className="text-3xl font-bold text-gray-950">
                        Upload Files
                    </h3>
                    <h4 className="text-gray-600 text-lg text-center">
                        Please upload the audio/video files that you would like
                        to transcribe.
                    </h4>
                </div>
                <Dropzone
                    onDrop={(acceptedFiles) =>
                        setFiles((prev) => [...prev, ...acceptedFiles])
                    }
                    accept={fileTypes}
                >
                    {({ getRootProps, getInputProps }) => (
                        <div
                            className="flex flex-col items-center justify-center w-[95%] h-full outline-dashed outline-2 outline-gray-400 rounded px-5 py-10 bg-gray-50 gap-5 cursor-pointer"
                            {...getRootProps()}
                        >
                            <input {...getInputProps()} />
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
                    )}
                </Dropzone>
            </div>
        </Fragment>
    );
}
