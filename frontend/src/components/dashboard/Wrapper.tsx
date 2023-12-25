import Image from "next/image";
import Topbar from "@/src/components/dashboard/Topbar";
import Notifications from "@/src/components/dashboard/Notifications";
import FileUploadModal from "@/src/components/dashboard/FileUploadModal";

type props = {
    children: string | JSX.Element | Array<JSX.Element> | React.ReactNode;
};

export default function Wrapper({ children }: props) {
    return (
        <section className="relative mx-auto flex flex-col h-full w-full items-start justify-end">
            <Topbar />
            <Notifications />
            <FileUploadModal />
            {children}
        </section>
    );
}
