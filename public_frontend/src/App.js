import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import HeaderAnnoucmentContextProvider from "./contexts/HeaderAnnoucmentContext";
import HamburgerContextProvider from "./contexts/HamburgerContext";
import SearchPanelContextProvider from "./contexts/SearchPanelContext";
import CartContextProvider from "./contexts/CartContext";

function App() {
    return (
        <CartContextProvider>
            <SearchPanelContextProvider>
                <HamburgerContextProvider>
                    <HeaderAnnoucmentContextProvider>
                        <Router>
                            <Routes>
                                <Route path="/" element={<Home />} />
                            </Routes>
                        </Router>
                    </HeaderAnnoucmentContextProvider>
                </HamburgerContextProvider>
            </SearchPanelContextProvider>
        </CartContextProvider>
    );
}

export default App;
