"use client";

import { useEffect } from "react";
import Image from "next/image";

import { cn } from "@/src/lib/utils";

interface BaseModalUIProps {
    className?: string;
    children: string | JSX.Element | Array<JSX.Element> | React.ReactNode;
}

const ModalUI = ({ className, children }: BaseModalUIProps) => {
    useEffect(() => {
        document.body.style.overflow = "hidden";

        return () => {
            document.body.style.overflow = "auto";
        };
    }, []);

    return (
        <div
            className={cn(
                "fixed inset-0 z-[9999] flex h-full min-h-screen w-screen items-center justify-center overflow-auto border-2 bg-[url('/images/noise.png')] backdrop-blur-lg",
                className
            )}
        >
            {children}
        </div>
    );
};

interface ModalBodyUIProps extends BaseModalUIProps {
    onClose?: () => void;
}

const ModalBody = ({ onClose, className, children }: ModalBodyUIProps) => {
    return (
        <div
            className={cn(
                "relative flex flex-col items-center bg-white max-w-lg rounded gap-5 shadow px-8 py-5",
                className
            )}
        >
            {onClose ? (
                <Image
                    src="/icons/close.png"
                    alt="close"
                    width={30}
                    height={30}
                    onClick={onClose}
                    className="absolute top-4 right-4 cursor-pointer"
                />
            ) : null}
            {children}
        </div>
    );
};

const ModalHeader = ({ className, children }: BaseModalUIProps) => {
    return <div className={className}>{children}</div>;
};

const ModalContent = ({ className, children }: BaseModalUIProps) => {
    return <div className={cn("w-full h-full", className)}>{children}</div>;
};

ModalUI.Body = ModalBody;
ModalUI.Header = ModalHeader;
ModalUI.Content = ModalContent;

import useModalStore from "@/src/store/modal";

const Modal = () => {
    const { modal } = useModalStore();

    return modal;
};

export { ModalUI, Modal };
