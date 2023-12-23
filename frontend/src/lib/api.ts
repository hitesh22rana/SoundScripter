import { FileData } from "@/src/types/api";

const API_URL = "http://127.0.0.1:8000/api/v1";

export async function fileUpload({ file, name }: FileData) {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("name", name);

    const res = await (
        await fetch(API_URL + "/files/upload", {
            method: "POST",
            body: formData,
        })
    ).json();

    return res;
}
