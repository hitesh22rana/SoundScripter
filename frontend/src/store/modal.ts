import { create } from 'zustand';
import { createTrackedSelector } from 'react-tracked';

interface ModalStoreType {
    modal: JSX.Element | null;

    mountModal: (modal: JSX.Element) => void;
    unMountModal: () => void;
}

const useModalStoreZusatnd = create<ModalStoreType>((set) => ({
    modal: null,

    mountModal: (modal) => set(() => ({ modal: modal })),
    unMountModal: () => set(() => ({ modal: null })),
}));

const useModalStore = createTrackedSelector(useModalStoreZusatnd);
export default useModalStore;
