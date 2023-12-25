import { create } from "zustand";

import { fetchTranscriptionList } from "@/src/lib/api";
import { ListTranscription } from "@/src/types/api";

interface FileStoreType {
    error: string | null;
    data: ListTranscription[] | null;

    fetchTranscriptions: () => void;
}

const useTranscriptionStore = create<FileStoreType>((set, get) => ({
    error: null,
    data: null,

    fetchTranscriptions: async () => {
        try {
            const res = await fetchTranscriptionList();

            set(() => ({ data: res }));
        } catch (error) {
            set(() => ({ error: "Unable to fetch transcriptions" }));
        }
    },
}));

export default useTranscriptionStore;
