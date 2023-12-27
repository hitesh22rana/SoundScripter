import { create } from "zustand";

interface ModalStoreType {
    modal: JSX.Element | null;

    mountModal: (modal: JSX.Element) => void;
    unMountModal: () => void;
}

const useModalStore = create<ModalStoreType>((set) => ({
    modal: null,

    mountModal: (modal) => set(() => ({ modal: modal })),
    unMountModal: () => set(() => ({ modal: null })),
}));

export default useModalStore;
