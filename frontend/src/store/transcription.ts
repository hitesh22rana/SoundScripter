import { create } from "zustand";

import { fetchTranscriptionList } from "@/src/lib/api";
import { ListTranscriptionApiResponse } from "@/src/types/api";

interface FileStoreType {
    error: string | null;
    data: ListTranscriptionApiResponse[] | null;

    fetchTranscriptions: () => void;
    // generateTranscriptions: (payload) => void;
}

const useTranscriptionStore = create<FileStoreType>((set, get) => ({
    error: null,
    data: null,

    fetchTranscriptions: async () => {
        try {
            const res = await fetchTranscriptionList();
            set(() => ({ data: res }));
        } catch (error: any) {
            set(() => ({
                error: error.message || "Unable to fetch transcriptions",
            }));
        }
    },

    // generateTranscriptions: async () => {

    // }
}));

export default useTranscriptionStore;
