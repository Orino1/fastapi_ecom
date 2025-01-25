import { useContext, createContext, useState } from "react";

const context = createContext();

export const useCartContext = () => useContext(context);

export default function CartContextProvider({ children }) {
    const [isOpen, setIsOpen] = useState(false);
    const [currentView, setCurrentView] = useState("cart");
    const [cartItems, setCartItems] = useState([]);
    const [wishlistItems, setWishlistItems] = useState([]);

    // be used to open either cart or wishlist
    const openModal = (view) => {
        setCurrentView(view);
        setIsOpen(true);
    };

    //
    const closeModal = () => {
        setIsOpen(false);
    };

    return (
        <context.Provider
            value={{
                isOpen,
                currentView,
                cartItems,
                setCartItems,
                wishlistItems,
                setWishlistItems,
                openModal,
                closeModal,
            }}
        >
            {children}
        </context.Provider>
    );
}
