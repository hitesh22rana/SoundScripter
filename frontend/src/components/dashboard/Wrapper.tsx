import { Fragment } from "react";
import Image from "next/image";
import { Toaster } from "@/src/components/ui/sonner";
import Topbar from "@/src/components/dashboard/Topbar";
import { Modal } from "@/src/components/ui/modal";
import BackgroundProgressTracker from "./BackgroundProgressTracker";

type props = {
    children: string | JSX.Element | Array<JSX.Element> | React.ReactNode;
};

export default function Wrapper({ children }: props) {
    return (
        <Fragment>
            <main className="relative mx-auto flex flex-col h-full w-full items-start justify-end">
                <Topbar />
                {children}
            </main>
            <Toaster closeButton theme="light" />
            <Modal />
            <BackgroundProgressTracker />
            <Image
                src="/images/logo.png"
                width="300"
                height="300"
                alt="logo"
                priority
                draggable={false}
                quality={100}
                className="absolute w-auto h-auto top-1/2 left-1/2 right-1/2 -translate-x-1/2 -translate-y-1/2 bg-contain object-contain opacity-5 -z-50"
            />
        </Fragment>
    );
}
