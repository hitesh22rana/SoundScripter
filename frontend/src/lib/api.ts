import { FileData } from "@/src/types/api";
import { Sort } from "@/src/types/core";

const API_URL = "http://127.0.0.1:8000/api/v1";

export async function fileUpload({ file, name }: FileData) {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("name", name);

    const res = await (
        await fetch(API_URL + "/files", {
            method: "POST",
            body: formData,
        })
    ).json();

    return res;
}

export async function fetchFileList(
    limit: number = 100,
    offset: number = 0,
    sort: Sort = "DESC"
) {
    const res = await (
        await fetch(
            API_URL + `/files?limit=${limit}&offset=${offset}&sort=${sort}`,
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            }
        )
    ).json();

    return res.data;
}

export async function deleteFile(id: string) {
    const res = await (
        await fetch(API_URL + "/files/" + id, {
            method: "DELETE",
        })
    ).json();

    return res;
}

export async function fetchTranscriptionList(
    limit: number = 100,
    offset: number = 0,
    sort: Sort = "DESC"
) {
    const res = await (
        await fetch(
            API_URL +
                `/transcriptions?limit=${limit}&offset=${offset}&sort=${sort}`,
            {
                method: "GET",
            }
        )
    ).json();

    return res.data;
}
