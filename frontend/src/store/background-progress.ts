import { create } from 'zustand';
import { createTrackedSelector } from 'react-tracked';

interface BackgroundProgressStoreType {
    activeProgress: JSX.Element[];

    addToProgressTracker: (backgroundProgress: JSX.Element) => void;
    removeFromProgressTracker: (id: number) => void;
}

const useBackgroundProgressStoreZustand = create<BackgroundProgressStoreType>(
    (set, get) => ({
        activeProgress: [],
        addToProgressTracker: (backgroundProgress) => {
            const currentProgressTracker = get().activeProgress;

            set(() => ({
                activeProgress: [...currentProgressTracker, backgroundProgress],
            }));
        },
        removeFromProgressTracker: (id: number) => {
            const currentProgressTracker = get().activeProgress;
            if (!currentProgressTracker) return;

            const filteredProgressTracker = currentProgressTracker.filter(
                (backgroundProgress) => {
                    if (backgroundProgress.props.id === id) {
                        return false;
                    }

                    return true;
                },
            );

            set(() => ({
                activeProgress: filteredProgressTracker,
            }));
        },
    }),
);

const useBackgroundProgressStore = createTrackedSelector(
    useBackgroundProgressStoreZustand,
);
export default useBackgroundProgressStore;
