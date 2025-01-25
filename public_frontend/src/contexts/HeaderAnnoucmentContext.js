import { useContext, createContext } from "react";
import { useState } from "react";

const context = createContext();

export const useHeaderAnnoucmetContext = () => useContext(context);

export default function HeaderAnnoucmentContextProvider({ children }) {
    const [announcement, setAnnouncement] = useState("this is just a quick test");

    // usign the useEffect hoock we gonna call the api and set the annoucment at the start if there is any

    return (
        <context.Provider value={{ announcement, setAnnouncement }}>
            {children}
        </context.Provider>
    );
}
