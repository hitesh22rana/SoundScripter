import type { Metadata } from "next";
import { Open_Sans } from "next/font/google";

import Wrapper from "@/src/components/dashboard/Wrapper";

import "@/src/globals.css";

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

const MetaInfo = () => {
    return (
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
    );
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <MetaInfo />
            <body className={Font.className}>
                <Wrapper>{children}</Wrapper>
            </body>
        </html>
    );
}
