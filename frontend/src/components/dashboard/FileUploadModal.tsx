"use client";

import { useState } from "react";
import Image from "next/image";
import Dropzone, { Accept } from "react-dropzone";
import { toast } from "sonner";
import BackgroundProgress from "@/src/components/dashboard/BackgroundProgress";
import { ModalUI } from "@/src/components/ui/modal";
import { Button } from "@/src/components/ui/button";
import Input from "@/src/components/ui/input";

import useModalStore from "@/src/store/modal";
import useBackgroundProgressStore from "@/src/store/background-progress";
import { FileUploadApiPayload } from "@/src/types/api";

const fileTypes: Accept = {
    "audio/wav": [],
    "audio/mpeg": [],
    "video/mp4": [],
    "video/x-matroska": [],
};

const FileUploadModal = () => {
    const { unMountModal } = useModalStore();
    const { addToProgressTracker } = useBackgroundProgressStore();

    const [fileUploadApiPayload, setFileUploadApiPayload] =
        useState<FileUploadApiPayload>({} as FileUploadApiPayload);

    function handleFileNameChange(name: string) {
        setFileUploadApiPayload({ ...fileUploadApiPayload, name: name });
    }

    async function handleFileUpload() {
        if (!fileUploadApiPayload.file || !fileUploadApiPayload.name) return;

        const formData = new FormData();
        formData.append("file", fileUploadApiPayload.file);
        formData.append("name", fileUploadApiPayload.name);

        toast.info("Info", {
            description: "Uploading file",
        });

        addToProgressTracker(
            <BackgroundProgress
                url={process.env.NEXT_PUBLIC_BACKEND_API_URL + "/files"}
                method="POST"
                fileName={fileUploadApiPayload.name}
                payload={formData}
            />
        );
    }

    return (
        <ModalUI onClose={unMountModal}>
            <ModalUI.Header className="flex flex-col items-center justify-center gap-2">
                <ModalUI.Heading>Upload File</ModalUI.Heading>
                <ModalUI.SubHeading>
                    Please browse your folders or drag and drop your file here
                </ModalUI.SubHeading>
            </ModalUI.Header>

            <ModalUI.Body className="flex flex-col gap-5">
                <Dropzone
                    onDrop={(acceptedFiles) => {
                        const selectedFile =
                            acceptedFiles[acceptedFiles.length - 1];
                        setFileUploadApiPayload({
                            file: selectedFile,
                            name:
                                selectedFile?.name
                                    .split(".")[0]
                                    .toLocaleLowerCase() ?? "",
                        });
                    }}
                    accept={fileTypes}
                    maxFiles={1}
                >
                    {({ getRootProps, getInputProps }) => (
                        <div
                            className="flex flex-col items-center justify-center w-full h-full outline-dashed outline-2 outline-gray-400 rounded p-5 bg-gray-50 md:gap-3 gap-2 cursor-pointer"
                            {...getRootProps()}
                        >
                            <input {...getInputProps()} />
                            <Image
                                src="/icons/upload-dnd.svg"
                                alt="upload-dnd"
                                width={50}
                                height={50}
                                className="w-auto h-auto md:scale-150 scale-125"
                            />
                            <div className="flex flex-col items-center gap-0">
                                <span className="text-gray-950 font- md:text-base text-sm">
                                    Drag and Drop to upload files
                                </span>
                                <span>or</span>
                            </div>

                            <Button
                                variant="outline"
                                className="md:px-8 md:py-4 px-6 py-2 border-2 font-medium"
                            >
                                Browse
                            </Button>

                            <span className="text-gray-500 md:text-base text-sm">
                                Supported formats: wav, mp3, mp4, mkv
                            </span>
                        </div>
                    )}
                </Dropzone>
                <Input
                    name="name"
                    type="text"
                    value={fileUploadApiPayload.name}
                    placeholder="Enter file name"
                    onChange={(e) => handleFileNameChange(e.target.value)}
                />
                <Button
                    variant="default"
                    className="md:py-6 py-5 w-full md:text-lg mt-2 font-medium disabled:opacity-90 disabled:pointer-events-auto disabled:cursor-not-allowed text-base"
                    onClick={handleFileUpload}
                    disabled={
                        !fileUploadApiPayload.file || !fileUploadApiPayload.name
                    }
                >
                    Upload
                </Button>
            </ModalUI.Body>
        </ModalUI>
    );
};

export default FileUploadModal;
