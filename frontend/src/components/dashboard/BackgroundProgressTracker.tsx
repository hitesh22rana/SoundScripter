'use client';

import { Fragment, useEffect, useState } from 'react';
import Image from 'next/image';
import { Minimize2, Maximize2 } from 'lucide-react';

import { cn } from '@/src/lib/utils';
import useBackgroundProgressStore from '@/src/store/background-progress';

const BackgroundProgressTracker = () => {
    const { activeProgress } = useBackgroundProgressStore();
    const [fold, setFold] = useState<boolean>(true);

    useEffect(() => {
        if (activeProgress.length > 0) {
            setFold(false);
        } else {
            setFold(true);
        }
    }, [activeProgress]);

    return (
        <div
            className={cn(
                'fixed left-1/2 right-1/2 -translate-x-1/2 bottom-0 max-w-xl w-full h-56 rounded-t-2xl bg-gray-50 border-2 shadow-lg flex flex-col z-50 transition-all delay-100 ease-in-out pb-4',
                fold && 'h-16',
            )}
        >
            <div className="flex items-center justify-center w-full my-2 p-2">
                <h3
                    className={cn(
                        'cursor-pointer text-2xl font-semibold',
                        activeProgress.length > 0 && 'animate-pulse',
                    )}
                    onClick={() => setFold((prev) => !prev)}
                >
                    Upload Progress
                </h3>

                <div className="absolute right-4">
                    <Maximize2
                        className={cn(
                            !fold && 'hidden',
                            'cursor-pointer w-7 h-7 text-gray-500 bg-gray-100 rounded-md border',
                        )}
                        onClick={() => setFold(false)}
                    />
                    <Minimize2
                        className={cn(
                            fold && 'hidden',
                            'cursor-pointer w-7 h-7 text-gray-500 bg-gray-100 rounded-md border',
                        )}
                        onClick={() => setFold(true)}
                    />
                </div>
            </div>

            <div
                className={cn(
                    'flex flex-col items-start gap-2 px-4 overflow-auto',
                    fold && 'hidden',
                )}
            >
                <Image
                    src="/images/no-results-found.gif"
                    width="150"
                    height="150"
                    alt="No results found"
                    className={cn(
                        'mx-auto scale-125',
                        activeProgress.length > 0 && 'hidden',
                    )}
                    draggable={false}
                />

                {activeProgress.map((backgroundProgress) => {
                    return (
                        <Fragment key={backgroundProgress.props?.id}>
                            {backgroundProgress}
                        </Fragment>
                    );
                })}
            </div>
        </div>
    );
};

export default BackgroundProgressTracker;
