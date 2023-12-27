import type { Metadata } from "next";
import Image from "next/image";
import { Open_Sans } from "next/font/google";
import { ToastContainer } from "react-toastify";

import Wrapper from "@/src/components/dashboard/Wrapper";

import "@/src/globals.css";
import "react-toastify/dist/ReactToastify.css";

export const Font = Open_Sans({
    weight: ["400", "500", "600", "700", "800"],
    subsets: [
        "cyrillic",
        "cyrillic-ext",
        "greek",
        "greek-ext",
        "hebrew",
        "latin",
        "latin-ext",
        "vietnamese",
    ],
});

export const metadata: Metadata = {
    title: "SoundScripter",
    description:
        "Simplify and Automate your transcription workflow with SoundScripter",
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <head>
                <link
                    rel="apple-touch-icon"
                    sizes="180x180"
                    href="/apple-touch-icon.png"
                />
                <link
                    rel="icon"
                    type="image/png"
                    sizes="32x32"
                    href="/favicon-32x32.png"
                />
                <link
                    rel="icon"
                    type="image/png"
                    sizes="16x16"
                    href="/favicon-16x16.png"
                />
                <link rel="manifest" href="/site.webmanifest" />
                <link
                    rel="mask-icon"
                    href="/safari-pinned-tab.svg"
                    color="#5bbad5"
                />
                <meta name="msapplication-TileColor" content="#da532c" />
                <meta name="theme-color" content="#ffffff" />
            </head>
            <body className={Font.className}>
                <ToastContainer
                    position="top-center"
                    autoClose={2000}
                    hideProgressBar={false}
                    newestOnTop={true}
                    closeOnClick
                    rtl={false}
                    pauseOnFocusLoss
                    draggable
                    pauseOnHover
                    theme="light"
                    style={{ zIndex: 9999999 }}
                />
                <Image
                    src="/images/logo.png"
                    width="400"
                    height="400"
                    alt="logo"
                    priority
                    draggable={false}
                    quality={100}
                    className="absolute mnd:w-auto md:h-auto top-1/2 left-1/2 right-1/2 -translate-x-1/2 -translate-y-1/2 bg-contain object-contain opacity-5 -z-50"
                />
                <Wrapper>{children}</Wrapper>
            </body>
        </html>
    );
}
