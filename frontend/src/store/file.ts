import { create } from "zustand";

import { deleteFile, fetchFileList } from "@/src/lib/api";
import { ListFile } from "@/src/types/api";

interface FileStoreType {
    error: string | null;
    data: ListFile[] | null;

    fetchFiles: () => void;
    deleteFile: (id: string, revalidate: boolean) => void;
}

const useFileStore = create<FileStoreType>((set, get) => ({
    error: null,
    data: null,

    fetchFiles: async () => {
        set(() => ({ data: null, error: null }));

        try {
            const res = await fetchFileList();
            set(() => ({ data: res }));
        } catch (error) {
            set(() => ({ error: "Unable to fetch files data" }));
        }
    },
    deleteFile: async (id: string, revalidate: boolean) => {
        try {
            await deleteFile(id);
            if (revalidate) {
                get().fetchFiles();
            }
        } catch (error) {
            set(() => ({ error: "Unable to delete file" }));
        }
    },
}));

export default useFileStore;
