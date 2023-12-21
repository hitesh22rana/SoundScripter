"use client";

import { useState } from "react";
import Image from "next/image";
import Dropzone, { Accept } from "react-dropzone";

import Modal from "@/src/components/ui/modal";
import { Button } from "@/src/components/ui/button";

import useModalStore from "@/src/store/modal";

const fileTypes: Accept = {
    "audio/wav": [],
    "audio/mpeg": [],
    "video/mp4": [],
    "video/x-matroska": [],
};

const FileUploadModal = () => {
    const { isOpen, toggleModal } = useModalStore();
    const [file, setFile] = useState<File>();

    if (!isOpen) return null;

    const handleClose = () => {
        toggleModal();
    };

    return (
        <Modal isOpen={isOpen}>
            <div className="relative flex flex-col items-center bg-white max-w-lg rounded gap-10 shadow p-8">
                <div className="top-4 right-4 absolute">X</div>
                <div className="flex flex-col items-center justify-center gap-4">
                    <h3 className="text-3xl font-bold text-gray-950">
                        Upload File
                    </h3>
                    <h4 className="text-gray-600 text-lg text-center">
                        Please browse your folders or drag and drop your file
                        here, that you would like to transcribe.
                    </h4>
                </div>
                <Dropzone
                    onDrop={(acceptedFiles) => {
                        setFile(acceptedFiles[acceptedFiles.length - 1]);
                    }}
                    accept={fileTypes}
                    maxFiles={1}
                >
                    {({ getRootProps, getInputProps }) => (
                        <div
                            className="flex flex-col items-center justify-center w-full h-full outline-dashed outline-2 outline-gray-400 rounded p-5 bg-gray-50 gap-5 mb-2 cursor-pointer"
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
                                Browse
                            </Button>

                            <span className="text-gray-500">
                                Supported formats: wav, mp3, mp4, mkv
                            </span>
                        </div>
                    )}
                </Dropzone>
            </div>
        </Modal>
    );
};

export default FileUploadModal;
