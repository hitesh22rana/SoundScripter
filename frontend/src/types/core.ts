export type Status = 'QUEUE' | 'PROCESSING' | 'DONE' | 'ERROR';
export type Media = 'AUDIO' | 'VIDEO';
export type Priorty = 'LOW' | 'MEDIUM' | 'HIGH';
export type Sort = 'ASC' | 'DESC';
export type NotificationType = 'INFO' | 'SUCCESS' | 'ERROR';
export type Task =
    | 'CONVERSION'
    | 'OPTIMIZATION'
    | 'TRANSCRIPTION'
    | 'TERMINATE';
export type Language = 'en';
