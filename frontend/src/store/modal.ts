import { create } from "zustand";

interface ModalStoreType {
    isOpen: boolean;

    toggleModal(): void;
}

const useModalStore = create<ModalStoreType>((set, get) => ({
    isOpen: true,

    toggleModal: () => set(() => ({ isOpen: !get().isOpen })),
}));

export default useModalStore;
