import { useState, useContext, createContext } from "react";

const context = createContext();

export const useHamburgerContext = () => useContext(context);

export default function HamburgerContextProvider({ children }) {
    const [menuOpen, setMenuOpen] = useState(false);

    return <context.Provider value={{menuOpen, setMenuOpen}}>{children}</context.Provider>;
}
