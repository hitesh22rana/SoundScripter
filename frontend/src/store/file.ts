import { create } from "zustand";

import { deleteFile, fetchFileList } from "@/src/lib/api";
import { ListFileApiResponse } from "@/src/types/api";
import { Status } from "@/src/types/core";

interface FileStoreType {
    dataError: string | null;
    data: ListFileApiResponse[] | null;

    fetchFiles: () => void;
    deleteFile: (id: string, revalidate: boolean) => void;
    updateFilesDataProgress: (
        id: string,
        status: Status,
        completed_at: string | null
    ) => void;
}

const useFileStore = create<FileStoreType>((set, get) => ({
    dataError: null,
    data: null,

    fetchFiles: async () => {
        try {
            const res = await fetchFileList();
            set(() => ({ data: res }));
        } catch (error: any) {
            set(() => ({
                dataError: error.message || "Unable to fetch files data",
            }));
        }
    },
    deleteFile: async (id: string, revalidate: boolean) => {
        try {
            await deleteFile(id);
            const data = get().data;
            if (!data) return;
            set(() => ({ data: data.filter((file) => file.id !== id) }));

            if (revalidate) {
                get().fetchFiles();
            }
        } catch (error: any) {
            throw new Error(error?.detail || "Unable to delete file");
        }
    },
    updateFilesDataProgress: (
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
}));

export default useFileStore;
