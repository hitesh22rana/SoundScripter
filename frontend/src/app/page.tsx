"use client";

import { useState } from "react";
import Image from "next/image";

import { Button } from "@/src/components/ui/button";
import useModalStore from "@/srcstore/modal";

export default function Page() {
    const { toggleModal } = useModalStore();
    const [listType, setListType] = useState<string>("files");

    return (
        <section className="flex flex-col items-start justify-start p-2">
            <Button
                variant="default"
                className="p-5 border-2 font-medium gap-2"
                onClick={toggleModal}
            >
                <Image
                    src="/icons/upload.svg"
                    alt="Upload"
                    width={20}
                    height={20}
                />
                Upload File
            </Button>
        </section>
    );
}
