'use client';

import { toast } from 'sonner';
import { Button } from '@/src/components/ui/button';
import { ModalUI } from '@/src/components/ui/modal';

import useModalStore from '@/src/store/modal';
import { TranscriptionApiResponse } from '@/src/types/api';
import useTranscriptionStore from '@/srcstore/transcription';

const TranscriptionTerminateModal = (
    transcription: TranscriptionApiResponse,
) => {
    const { unMountModal } = useModalStore();
    const { terminateTranscription } = useTranscriptionStore();

    async function handleTranscriptionTerminate(id: string) {
        try {
            await terminateTranscription(id);

            toast.success('Success', {
                description: 'File terminated successfully',
            });
        } catch (error: any) {
            toast.error('Error', {
                description:
                    error?.message || 'Failed to terminate transcription',
            });
        } finally {
            unMountModal();
        }
    }

    return (
        <ModalUI onClose={unMountModal}>
            <ModalUI.Header className="flex flex-col items-center justify-center gap-2">
                <ModalUI.Heading>Terminate Transcription</ModalUI.Heading>
                <ModalUI.SubHeading>
                    Are you sure you want to terminate this running
                    transcription?
                </ModalUI.SubHeading>
            </ModalUI.Header>

            <ModalUI.Body className="flex flex-col items-center justify-center gap-5 mt-2">
                <div className="flex flex-row justify-start gap-2 w-full">
                    <span className="text-base font-semibold min-w-max">
                        File name:
                    </span>
                    <span className="line-clamp-1">{transcription.name}</span>
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
                        onClick={() =>
                            handleTranscriptionTerminate(transcription.id)
                        }
                    >
                        Terminate
                    </Button>
                </div>
            </ModalUI.Body>
        </ModalUI>
    );
};

export default TranscriptionTerminateModal;
