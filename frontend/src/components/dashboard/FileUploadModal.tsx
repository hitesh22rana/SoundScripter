"use client";

import { useState } from "react";
import Image from "next/image";
import Dropzone, { Accept } from "react-dropzone";
import { toast } from "react-toastify";

import { ModalUI } from "@/src/components/ui/modal";
import { Button } from "@/src/components/ui/button";
import Input from "@/src/components/ui/input";

import useModalStore from "@/src/store/modal";
import useFileStore from "@/src/store/file";
import { FileData } from "@/src/types/api";
import { fileUpload } from "@/src/lib/api";

const fileTypes: Accept = {
    "audio/wav": [],
    "audio/mpeg": [],
    "video/mp4": [],
    "video/x-matroska": [],
};

const FileUploadModal = () => {
    const { unMountModal } = useModalStore();
    const { fetchFiles } = useFileStore();
    const [fileData, setFileData] = useState<FileData>({} as FileData);

    function handleFileNameChange(name: string) {
        setFileData({ ...fileData, name: name });
    }

    async function handleFileUpload() {
        if (!fileData?.file || !fileData.name) return;

        try {
            toast.info("Uploading file...");
            await fileUpload(fileData);
            fetchFiles();
            toast.success("File uploaded successfully");
        } catch (error) {
            toast.error("Error uploading file");
        }
    }

    return (
        <ModalUI>
            <ModalUI.Body onClose={unMountModal}>
                <ModalUI.Header className="flex flex-col items-center justify-center gap-2">
                    <h3 className="text-3xl font-bold text-gray-950">
                        Upload File
                    </h3>
                    <h4 className="text-gray-600 text-lg text-center">
                        Please browse your folders or drag and drop your file
                        here, that you would like to transcribe.
                    </h4>
                </ModalUI.Header>

                <ModalUI.Content className="flex flex-col gap-5">
                    <Dropzone
                        onDrop={(acceptedFiles) => {
                            const selectedFile =
                                acceptedFiles[acceptedFiles.length - 1];
                            setFileData({
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
                                className="flex flex-col items-center justify-center w-full h-full outline-dashed outline-2 outline-gray-400 rounded p-5 bg-gray-50 gap-4 cursor-pointer"
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
                                    className="px-8 py-4 border-2 font-medium"
                                >
                                    Browse
                                </Button>

                                <span className="text-gray-500">
                                    Supported formats: wav, mp3, mp4, mkv
                                </span>
                            </div>
                        )}
                    </Dropzone>
                    <Input
                        name="name"
                        type="text"
                        value={fileData.name}
                        placeholder="Name"
                        onChange={(e) => handleFileNameChange(e.target.value)}
                    />
                    <Button
                        variant="default"
                        className="py-6 w-full text-lg font-medium"
                        onClick={handleFileUpload}
                    >
                        Upload
                    </Button>
                </ModalUI.Content>
            </ModalUI.Body>
        </ModalUI>
    );
};

export default FileUploadModal;
