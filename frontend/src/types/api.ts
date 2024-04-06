import { Language, Media, Priorty, Status } from '@/src/types/core';

export type FileUploadApiPayload = {
    file: File;
    name: string;
    type: Media;
    size: number;
};

export type FileApiResponse = {
    id: string;
    name: string;
    type: Media;
    status: Status;
    created_at: Date;
    completed_at: Date;
};

export type TranscriptionApiResponse = {
    id: string;
    name: string;
    type: Media;
    task_ids: string[];
    language: string;
    priority: Priorty;
    status: Status;
    created_at: Date;
    completed_at: Date;
};

export type TranscribeFileApiPayload = {
    file_id: string;
    language: Language;
    priority: Priorty;
};
