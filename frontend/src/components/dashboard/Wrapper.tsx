import Image from 'next/image';
import Topbar from '@/src/components/dashboard/Topbar';

type props = {
    children: string | JSX.Element | Array<JSX.Element> | React.ReactNode;
};

export default function Wrapper({ children }: props) {
    return (
        <main className="relative mx-auto flex flex-col min-h-screen h-full w-full items-start justify-start">
            <Image
                src="/images/logo.png"
                width="300"
                height="300"
                alt="logo"
                priority
                draggable={false}
                quality={100}
                className="absolute top-1/2 left-1/2 right-1/2 -translate-x-1/2 -translate-y-1/2 bg-contain object-contain opacity-5 -z-50"
            />
            <Topbar />
            {children}
        </main>
    );
}
