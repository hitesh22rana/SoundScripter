import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

import { Media } from '@/src/types/core';

export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

export const dateFormatOptions = {
    year: 'numeric',
    month: 'numeric',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
};

export function isError(statusCode: number): boolean {
    return statusCode >= 400;
}

export function extractMediaType(mediaType: string): Media | null {
    const parts = mediaType.split('/');

    if (parts.length !== 2) {
        return null;
    }

    const mainType = parts[0].toLowerCase();
    switch (mainType) {
        case 'audio':
            return 'AUDIO';
        case 'video':
            return 'VIDEO';
        default:
            return null;
    }
}

export function humanReadableSize(sizeInBytes: number): string {
    const units = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
    let i = 0;
    let f = sizeInBytes;

    if (sizeInBytes === 0) {
        return '0 B';
    }

    while (f >= 1024 && i < units.length - 1) {
        f /= 1024;
        i++;
    }

    f = Math.round(f * 10) / 10;

    return `${f} ${units[i]}`;
}

export function getFormattedDate(): string {
    const today = new Date();

    const formattedDate = new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
    }).format(today);

    return formattedDate;
}
