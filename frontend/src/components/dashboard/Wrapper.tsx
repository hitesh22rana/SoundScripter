import Topbar from "@/src/components/dashboard/Topbar";
import { Modal } from "@/src/components/ui/modal";

type props = {
    children: string | JSX.Element | Array<JSX.Element> | React.ReactNode;
};

export default function Wrapper({ children }: props) {
    return (
        <section className="relative mx-auto flex flex-col h-full w-full items-start justify-end">
            <Topbar />
            <Modal />
            {children}
        </section>
    );
}
