import { create } from "zustand";

interface BackgroundProgressStoreType {
    progressTracker: JSX.Element[] | null;

    addToProgressTracker: (backgroundProgress: JSX.Element) => void;
}

const useBackgroundProgressStore = create<BackgroundProgressStoreType>(
    (set, get) => ({
        progressTracker: null,
        addToProgressTracker: (backgroundProgress) => {
            const currentProgressTracker = get().progressTracker;

            if (!currentProgressTracker) {
                return set(() => ({
                    progressTracker: [backgroundProgress],
                }));
            }

            set(() => ({
                progressTracker: [
                    ...currentProgressTracker,
                    backgroundProgress,
                ],
            }));
        },
    })
);

export default useBackgroundProgressStore;
