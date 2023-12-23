"use client";

import { useEffect } from "react";

interface Props {
    isOpen: boolean;
    children: string | JSX.Element | Array<JSX.Element> | React.ReactNode;
}

const Modal = ({ isOpen, children }: Props) => {
    useEffect(() => {
        if (isOpen) {
            document.body.style.overflow = "hidden";
        } else {
            document.body.style.overflow = "auto";
        }

        return () => {
            document.body.style.overflow = "auto";
        };
    }, [isOpen]);

    return (
        <div
            className={`fixed inset-0 z-[9999] flex h-full min-h-screen w-screen items-center justify-center overflow-auto border-2 bg-[url('/images/noise.png')] backdrop-blur-lg ${
                isOpen ? "block" : "hidden"
            }`}
        >
            {children}
        </div>
    );
};

export default Modal;
