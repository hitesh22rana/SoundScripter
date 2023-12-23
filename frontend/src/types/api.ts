export type FileData = {
    file: File;
    name: string;
};

export type Status = "QUEUE" | "PROCESSING" | "DONE" | "ERROR";

export type ListFile = {
    id: string;
    name: string;
    type: string;
    status: Status;
    created_at: Date;
    completed_at: Date;
};
