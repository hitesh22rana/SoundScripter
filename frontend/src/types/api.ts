import { Media, Priorty, Status } from "./core";

export type FileData = {
    file: File;
    name: string;
};

export type ListFile = {
    id: string;
    name: string;
    type: Media;
    status: Status;
    created_at: Date;
    completed_at: Date;
};

export type ListTranscription = {
    id: string;
    name: string;
    type: Media;
    task_id: string;
    language: string;
    priority: Priorty;
    status: Status;
    created_at: Date;
    completed_at: Date;
};
