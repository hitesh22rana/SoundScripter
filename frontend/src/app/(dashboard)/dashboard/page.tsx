import { Accept } from "react-dropzone";

import FileUpload from "@/src/components/ui/file-upload";

const fileTypes: Accept = {
    "audio/wav": [],
    "audio/mpeg": [],
    "video/mp4": [],
    "video/x-matroska": [],
};

export default function DashbordPage() {
    return (
        <section className="flex flex-col justify-between p-3">
            <FileUpload fileTypes={fileTypes} />
        </section>
    );
}
