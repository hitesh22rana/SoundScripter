import { create } from "zustand";

import {
    fetchTranscriptionList,
    downloadTranscription,
    terminateTranscription,
} from "@/src/lib/api";
import { TranscriptionApiResponse } from "@/src/types/api";
import { Status } from "@/src/types/core";

interface FileStoreType {
    error: string | null;
    data: TranscriptionApiResponse[] | null;

    fetchTranscriptions: () => void;
    updateTranscribeDataProgress: (
        id: string,
        status: Status,
        completed_at: string | null
    ) => void;
    downloadTranscription: (id: string, fileName: string) => void;
    terminateTranscription: (id: string) => void;
    removeTranscription: (id: string, field: "id" | "task_id") => void;
}

const useTranscriptionStore = create<FileStoreType>((set, get) => ({
    error: null,
    data: null,

    fetchTranscriptions: async () => {
        try {
            const { data } = await fetchTranscriptionList();
            set({ data: data, error: null });
        } catch (error: any) {
            set({
                data: null,
                error: error.message || "Failed to fetch transcriptions",
            });
        }
    },
    updateTranscribeDataProgress: (
        id: string,
        status: Status,
        completed_at: string | null
    ) => {
        const data = get().data;
        if (!data) return;

        data.map((file) => {
            if (file.id === id) {
                file.status = status;
                if (completed_at) {
                    file.completed_at = new Date(completed_at);
                }
            }
        });

        set(() => ({ data: [...data] }));
    },
    downloadTranscription: async (id: string, fileName: string) => {
        try {
            await downloadTranscription(id, fileName);
        } catch (error: any) {
            throw new Error(
                error?.detail || "Failed to download transcription"
            );
        }
    },
    terminateTranscription: async (id: string) => {
        try {
            await terminateTranscription(id);

            const data = get().data;
            if (!data) return;

            get().removeTranscription(id, "id");
        } catch (error: any) {
            throw new Error(
                error?.detail || "Failed to terminate transcription"
            );
        }
    },
    removeTranscription: (id: string, field: "id" | "task_id") => {
        const data = get().data;
        if (!data) return;

        set(() => ({
            data: data.filter((transcription) => transcription[field] !== id),
        }));
    },
}));

export default useTranscriptionStore;
