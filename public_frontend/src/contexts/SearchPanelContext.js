import { useState, createContext, useContext } from "react";

const context = createContext();

export const useSearchPanelContext = () => useContext(context);

export default function SearchPanelContextProvider({ children }) {
    const [searchPannelOpen, setSearchPannelOpen] = useState(false);

    return (
        <context.Provider value={{ searchPannelOpen, setSearchPannelOpen }}>
            {children}
        </context.Provider>
    );
}
