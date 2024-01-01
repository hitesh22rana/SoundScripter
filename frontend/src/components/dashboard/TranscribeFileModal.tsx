"use client";

import { useState } from "react";
import { toast } from "sonner";
import { ModalUI } from "@/src/components/ui/modal";
import { Button } from "@/src/components/ui/button";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/src/components/ui/select";

import useModalStore from "@/src/store/modal";
import { ListFileApiResponse, TranscribeFileApiPayload } from "@/src/types/api";
import { Language, Priorty } from "@/src/types/core";
import { transcribeFile } from "@/src/lib/api";

const TranscriptionFileModal = (file: ListFileApiResponse) => {
    const { unMountModal } = useModalStore();
    const [transibeFileApiPayload, setTranscribeFileApiPayload] =
        useState<TranscribeFileApiPayload>({} as TranscribeFileApiPayload);

    async function handleTranscribeFile() {
        if (
            !transibeFileApiPayload.language ||
            !transibeFileApiPayload.priority
        )
            return;

        try {
            await transcribeFile({
                file_id: file.id,
                language: transibeFileApiPayload.language,
                priority: transibeFileApiPayload.priority,
            });

            toast.success("Success", {
                description: "File added for transcription",
            });
        } catch (error: any) {
            toast.error("Error", {
                description: error?.message || "Something went wrong",
            });
        }
    }

    return (
        <ModalUI onClose={unMountModal} className="overflow-visible">
            <ModalUI.Header className="flex flex-col items-center justify-center gap-2">
                <ModalUI.Heading>Transcribe File</ModalUI.Heading>
                <ModalUI.SubHeading>
                    Select source language and priority
                </ModalUI.SubHeading>
            </ModalUI.Header>

            <ModalUI.Body className="flex flex-col gap-5">
                <div className="flex flex-row justify-between gap-2 w-full">
                    <span className="text-base font-semibold min-w-max">
                        File name:
                    </span>
                    <span className="text-ellipsis overflow-hidden whitespace-nowrap">
                        {file.name}
                    </span>
                </div>
                <div className="flex flex-row items-center justify-between">
                    <Select
                        onValueChange={(value) =>
                            setTranscribeFileApiPayload({
                                ...transibeFileApiPayload,
                                language: value as Language,
                            })
                        }
                    >
                        <SelectTrigger className="w-[180px] focus-within:ring-0 focus-within:outline-none focus-visible:ring-0">
                            <SelectValue placeholder="Language" />
                        </SelectTrigger>
                        <SelectContent className="z-[99999999]">
                            <SelectItem value="en">English</SelectItem>
                        </SelectContent>
                    </Select>
                    <Select
                        onValueChange={(value) =>
                            setTranscribeFileApiPayload({
                                ...transibeFileApiPayload,
                                priority: value as Priorty,
                            })
                        }
                    >
                        <SelectTrigger className="w-[180px] focus-within:ring-0 focus-within:outline-none focus-visible:ring-0">
                            <SelectValue placeholder="Priority" />
                        </SelectTrigger>
                        <SelectContent className="z-[99999999]">
                            <SelectItem value="LOW">Low</SelectItem>
                            <SelectItem value="HIGH">High</SelectItem>
                        </SelectContent>
                    </Select>
                </div>
                <Button
                    variant="default"
                    className="md:py-6 py-5 w-full md:text-lg mt-2 font-medium disabled:opacity-90 disabled:pointer-events-auto disabled:cursor-not-allowed text-base"
                    onClick={handleTranscribeFile}
                    disabled={
                        !transibeFileApiPayload.language ||
                        !transibeFileApiPayload.priority
                    }
                >
                    Transcribe
                </Button>
            </ModalUI.Body>
        </ModalUI>
    );
};

export default TranscriptionFileModal;
