"use client";

import { usePathname } from "next/navigation";

import Link from "next/link";
import Image from "next/image";

import { Button } from "@/src/components/ui/button";

import { TRoute } from "@/src/types/sidebar";
import { cn } from "@/src/lib/utils";

export default function Sidebar() {
    const pathName: string = usePathname();

    const routes: Array<TRoute> = [
        {
            name: "Upload",
            icon: "/icons/upload.svg",
            path: "/dashboard",
        },
        {
            name: "Transcriptions",
            icon: "/icons/transcription.svg",
            path: "/dashboard/transcriptions",
        },
    ];

    return (
        <aside className="fixed flex-col bg-white px-2 py-4 w-60 max-w-full flex bottom-0 left-0 top-0 z-[999] h-full min-h-screen items-center justify-between gap-5 overflow-auto shadow shadow-gray-200">
            <section className="flex flex-col h-full w-full gap-10">
                <h2 className="text-3xl font-bold text-gray-600 text-center">
                    SoundScripter
                </h2>

                <nav className="flex w-full flex-col gap-1">
                    {routes.map((route: TRoute, index: number) => {
                        return (
                            <Button
                                key={index}
                                asChild={true}
                                variant={
                                    route.path === pathName
                                        ? "secondary"
                                        : "ghost"
                                }
                                className={cn(
                                    "flex flex-row items-center justify-start gap-4 w-full py-6 font-semibold",
                                    route.path === pathName
                                        ? " text-gray-950"
                                        : "text-gray-600"
                                )}
                            >
                                <Link href={route.path}>
                                    <Image
                                        src={route.icon}
                                        height={25}
                                        width={25}
                                        alt={route.name}
                                    ></Image>
                                    {route.name}
                                </Link>
                            </Button>
                        );
                    })}
                </nav>
            </section>
        </aside>
    );
}
