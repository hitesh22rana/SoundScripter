import Image from "next/image";

export default function Topbar() {
    return (
        <header className="flex w-full h-auto flex-row items-center justify-between bg-white shadow-sm px-5 py-2">
            <Image
                src="/images/logo-icon.png"
                width="30"
                height="30"
                alt="logo"
                draggable={false}
                quality={100}
                className="w-auto h-auto bg-contain object-contain"
            />

            <div className="flex items-center justify-center rounded-full border p-0">
                <Image
                    src="/icons/notifications.png"
                    width="20"
                    height="20"
                    alt="notifications"
                    draggable={false}
                    quality={100}
                    className="w-auto h-auto bg-contain object-contain scale-75"
                />
            </div>
        </header>
    );
}
