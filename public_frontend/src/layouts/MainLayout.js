import styles from "../assets/styles/layouts/MainLayout.module.css";
import NavBar from "../components/NavBar";
import Footer from "../components/Footer";
import { useHeaderAnnoucmetContext } from "../contexts/HeaderAnnoucmentContext";
import HeaderAnnoucment from "../components/HeaderAnnoucment";
import { useHamburgerContext } from "../contexts/HamburgerContext";
import HamburgerMenu from "../components/HamburgerMenu";
import { useSearchPanelContext } from "../contexts/SearchPanelContext";
import SearchPanel from "../components/SearchPanel";
import { useCartContext } from "../contexts/CartContext";
import CartWishlistModal from "../components/CartWishlistModal";

export default function MainLayout({ children }) {
    const { announcement } = useHeaderAnnoucmetContext();
    const { menuOpen } = useHamburgerContext();
    const { searchPannelOpen } = useSearchPanelContext();
    const { isOpen } = useCartContext();

    return (
        <>
            {isOpen && <CartWishlistModal/>}
            {searchPannelOpen && <SearchPanel/>}
            {menuOpen && <HamburgerMenu />}
            {announcement && <HeaderAnnoucment />}
            <main className={styles.main}>
                <NavBar />
                <div className={styles.contentconatiner}>{children}</div>
                <Footer />
            </main>
        </>
    );
}
