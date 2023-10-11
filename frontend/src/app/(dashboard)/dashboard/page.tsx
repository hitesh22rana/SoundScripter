import FileUpload from "@/src/components/ui/file-upload";

export default function DashbordPage() {
    return (
        <section className="flex flex-col justify-between p-3">
            <FileUpload fileTypes={["wav", "mp3", "mp4", "mkv"]} />
        </section>
    );
}
