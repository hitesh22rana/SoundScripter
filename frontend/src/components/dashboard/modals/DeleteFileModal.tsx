'use client';

import { toast } from 'sonner';
import { Button } from '@/src/components/ui/button';
import { ModalUI } from '@/src/components/ui/modal';

import useModalStore from '@/src/store/modal';
import useFileStore from '@/src/store/file';
import { FileApiResponse } from '@/src/types/api';

const DeleteFileModal = (file: FileApiResponse) => {
    const { unMountModal } = useModalStore();
    const { deleteFile } = useFileStore();

    async function handleFileDelete(id: string) {
        try {
            await deleteFile(id, false);

            toast.success('Success', {
                description: 'File deleted successfully',
            });
        } catch (error: any) {
            toast.error('Error', {
                description: error?.message || 'Failed to delete file',
            });
        } finally {
            unMountModal();
        }
    }

    return (
        <ModalUI onClose={unMountModal}>
            <ModalUI.Header className="flex flex-col items-center justify-center gap-2">
                <ModalUI.Heading>Delete File</ModalUI.Heading>
                <ModalUI.SubHeading>
                    Are you sure you want to delete this file?
                </ModalUI.SubHeading>
            </ModalUI.Header>

            <ModalUI.Body className="flex flex-col items-center justify-center gap-5 mt-2">
                <div className="flex flex-row justify-start gap-2 w-full">
                    <span className="text-base font-semibold min-w-max">
                        File name:
                    </span>
                    <span className="line-clamp-1">{file.name}</span>
                </div>
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
                        className="w-full p-5 font-medium text-base"
                        onClick={() => handleFileDelete(file.id)}
                    >
                        Delete
                    </Button>
                </div>
            </ModalUI.Body>
        </ModalUI>
    );
};

export default DeleteFileModal;
