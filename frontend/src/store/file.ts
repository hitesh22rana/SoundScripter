import { create } from 'zustand';
import { createTrackedSelector } from 'react-tracked';

import { deleteFile, fetchFileList } from '@/src/lib/api';
import { FileApiResponse } from '@/src/types/api';
import { Status } from '@/src/types/core';

interface FileStoreType {
    data: FileApiResponse[] | null;

    fetchFiles: () => void;
    deleteFile: (id: string, revalidate: boolean) => void;
    updateFilesDataProgress: (
        id: string,
        status: Status,
        completed_at: string | null,
    ) => void;
}

const useFileStoreZustand = create<FileStoreType>((set, get) => ({
    data: null,

    fetchFiles: async () => {
        try {
            const { data } = await fetchFileList();
            set(() => ({ data: data }));
        } catch (error: any) {
            throw new Error(error?.detail || 'Failed to fetch files data');
        }
    },
    deleteFile: async (id: string, revalidate: boolean) => {
        try {
            await deleteFile(id);

            const data = structuredClone(get().data);
            if (!data) return;

            set(() => ({ data: data.filter((file) => file.id !== id) }));

            if (revalidate) {
                get().fetchFiles();
            }
        } catch (error: any) {
            throw new Error(error?.detail || 'Failed to delete file');
        }
    },
    updateFilesDataProgress: (
        id: string,
        status: Status,
        completed_at: string | null,
    ) => {
        const data = structuredClone(get().data);
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

const useFileStore = createTrackedSelector(useFileStoreZustand);
export default useFileStore;
