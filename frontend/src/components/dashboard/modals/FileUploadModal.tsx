'use client';

import { useState } from 'react';
import Dropzone, { Accept } from 'react-dropzone';
import { toast } from 'sonner';
import { UploadCloud } from 'lucide-react';
import BackgroundProgress from '@/src/components/dashboard/BackgroundProgress';
import { ModalUI } from '@/src/components/ui/modal';
import { Button } from '@/src/components/ui/button';
import Input from '@/src/components/ui/input';

import useModalStore from '@/src/store/modal';
import useBackgroundProgressStore from '@/src/store/background-progress';
import { FileUploadApiPayload } from '@/src/types/api';
import { extractMediaType } from '@/src/lib/utils';

const fileTypes: Accept = {
    'video/*': [],
    'audio/*': [],
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
        formData.append('file', fileUploadApiPayload.file);
        formData.append('name', fileUploadApiPayload.name);

        toast.info('Info', {
            description: 'Uploading file',
        });

        addToProgressTracker(
            <BackgroundProgress
                id={Date.now()}
                url={process.env.NEXT_PUBLIC_BACKEND_API_URL + '/files'}
                method="POST"
                fileName={fileUploadApiPayload.name}
                fileType={fileUploadApiPayload.type}
                fileSize={fileUploadApiPayload.size}
                payload={formData}
            />,
        );

        unMountModal();
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
                        const name =
                            selectedFile?.name
                                .split('.')[0]
                                .toLocaleLowerCase() ?? '';
                        const type = extractMediaType(selectedFile.type);
                        if (!type) {
                            toast.error('Error', {
                                description: 'Unsupported file type',
                            });
                            return;
                        }

                        setFileUploadApiPayload({
                            file: selectedFile,
                            name: name,
                            type: type,
                            size: selectedFile.size,
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
                            <UploadCloud className="md:w-12 md:h-12 w-10 h-10 text-gray-600" />
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
                <div className="flex flex-row w-full gap-2 items-center justify-evenly mt-4">
                    <Button
                        variant="outline"
                        className="w-full p-5 font-medium text-base"
                        onClick={unMountModal}
                    >
                        Cancel
                    </Button>
                    <Button
                        variant="default"
                        className="w-full p-5 font-medium text-base disabled:opacity-90 disabled:pointer-events-auto disabled:cursor-not-allowed"
                        onClick={handleFileUpload}
                        disabled={
                            !fileUploadApiPayload.file ||
                            !fileUploadApiPayload.name
                        }
                    >
                        Upload
                    </Button>
                </div>
            </ModalUI.Body>
        </ModalUI>
    );
};

export default FileUploadModal;
