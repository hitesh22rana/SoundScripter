'use client';

import { useEffect } from 'react';
import { X } from 'lucide-react';

import useModalStore from '@/src/store/modal';
import { cn } from '@/src/lib/utils';

interface BaseModalUIProps {
    className?: string;
    children: string | JSX.Element | Array<JSX.Element> | React.ReactNode;
}

interface ModalUIProps extends BaseModalUIProps {
    onClose?: () => void;
}

const ModalUI = ({ onClose, className, children }: ModalUIProps) => {
    useEffect(() => {
        document.body.style.overflow = 'hidden';

        return () => {
            document.body.style.overflow = 'auto';
        };
    }, []);

    return (
        <div className="fixed inset-0 z-[9999] flex h-full min-h-screen w-screen items-center justify-center overflow-auto bg-[url('/images/noise.png')] bg-black/30 p-0 backdrop-blur-lg">
            <div
                className={cn(
                    'relative flex flex-col items-center bg-white max-w-md md:w-full w-[95%] rounded gap-5 shadow-md md:px-6 px-5 md:py-5 py-4',
                    className,
                )}
            >
                {onClose ? (
                    <X
                        className="absolute md:top-5 md:right-4 top-4 right-3 md:scale-100 scale-75 cursor-pointer text-gray-600"
                        onClick={onClose}
                    />
                ) : null}
                {children}
            </div>
        </div>
    );
};

const ModalUIHeader = ({ className, children }: BaseModalUIProps) => {
    return <div className={cn('w-full h-full', className)}>{children}</div>;
};

const ModalUIHeading = ({ className, children }: BaseModalUIProps) => {
    return (
        <h3
            className={cn(
                'md:text-3xl text-2xl font-bold text-gray-950',
                className,
            )}
        >
            {children}
        </h3>
    );
};

const ModalUISubHeading = ({ className, children }: BaseModalUIProps) => {
    return (
        <h4
            className={cn(
                'text-gray-600 md:text-lg text-sm text-center',
                className,
            )}
        >
            {children}
        </h4>
    );
};

const ModalUIBody = ({ className, children }: BaseModalUIProps) => {
    return <div className={cn('w-full h-full', className)}>{children}</div>;
};

ModalUI.Header = ModalUIHeader;
ModalUI.Heading = ModalUIHeading;
ModalUI.SubHeading = ModalUISubHeading;
ModalUI.Body = ModalUIBody;

const Modal = () => {
    const { modal } = useModalStore();

    return modal;
};

export { ModalUI, Modal };
