import Image from 'next/image';
import Notifications from '@/src/components/dashboard/Notifications';

export default function Topbar() {
    return (
        <header className="flex w-full h-auto min-h-fit flex-row items-center justify-between shadow bg-gray-50 px-5 py-4">
            <Image
                src="/images/logo-icon.png"
                width="30"
                height="30"
                alt="logo"
                draggable={false}
                quality={100}
                className="bg-contain object-contain"
            />

            <Notifications />
        </header>
    );
}
