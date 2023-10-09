import FileUpload from "@/src/components/ui/file-upload";

export default function DashbordPage() {
    return (
        <section className="flex flex-col justify-between p-3">
            <FileUpload fileTypes={["WAV", "MP3", "MP4", "MKV", "MOV"]} />
        </section>
    );
}
