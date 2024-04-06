import { TranscribeFileApiPayload } from '@/src/types/api';
import { Sort } from '@/src/types/core';

const API_URL = process.env.NEXT_PUBLIC_BACKEND_API_URL;

export async function fetchFileList(
    limit: number = 100,
    offset: number = 0,
    sort: Sort = 'DESC',
) {
    const res = await fetch(
        API_URL + `/files?limit=${limit}&offset=${offset}&sort=${sort}`,
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        },
    );

    const data = await res.json();

    if (!res.ok) {
        throw new Error(data.detail || 'Something went wrong');
    }

    return data;
}

export async function deleteFile(id: string) {
    const res = await fetch(API_URL + '/files/' + id, {
        method: 'DELETE',
    });

    const data = await res.json();

    if (!res.ok) {
        throw new Error(data.detail || 'Something went wrong');
    }

    return data;
}

export async function fetchTranscriptionList(
    limit: number = 100,
    offset: number = 0,
    sort: Sort = 'DESC',
) {
    const res = await fetch(
        API_URL +
            `/transcriptions?limit=${limit}&offset=${offset}&sort=${sort}`,
        {
            method: 'GET',
        },
    );

    const data = await res.json();

    if (!res.ok) {
        throw new Error(data.detail || 'Something went wrong');
    }

    return data;
}

export async function transcribeFile(payload: TranscribeFileApiPayload) {
    const res = await fetch(API_URL + '/transcriptions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (!res.ok) {
        throw new Error(data.detail || 'Something went wrong');
    }

    return data;
}

export async function downloadTranscription(id: string, fileName: string) {
    const res = await fetch(API_URL + '/transcriptions/' + id + '/download', {
        method: 'GET',
    });

    if (!res.ok) {
        throw new Error('File download failed');
    }

    const blob = await res.blob();

    const downloadLink = document.createElement('a');

    const objectUrl = URL.createObjectURL(blob);

    downloadLink.href = objectUrl;

    downloadLink.download = fileName;

    downloadLink.click();

    URL.revokeObjectURL(objectUrl);

    return res;
}

export async function terminateTranscription(id: string) {
    const res = await fetch(API_URL + '/transcriptions/' + id + '/terminate', {
        method: 'DELETE',
    });

    const data = await res.json();

    if (!res.ok) {
        throw new Error(data.detail || 'Something went wrong');
    }

    return data;
}
