import Sidebar from "@/src/components/dashboard/Sidebar";
import Topbar from "./Topbar";

type props = {
    children: string | JSX.Element | Array<JSX.Element> | React.ReactNode;
};

export default function Wrapper({ children }: props) {
    return (
        <section className="relative mx-auto flex h-full w-full flex-row items-start justify-end">
            <Sidebar />
            <div className="flex h-full min-h-screen w-full flex-col max-w-[calc(100%-15rem)]">
                <Topbar />
                {children}
            </div>
        </section>
    );
}
