import styles from "../assets/styles/componenets/NavBar.module.css";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import { useHamburgerContext } from "../contexts/HamburgerContext";
import { useSearchPanelContext } from "../contexts/SearchPanelContext";
import { useCartContext } from "../contexts/CartContext";

export default function NavBar() {
    const [navbarFixed, setNavbarFixed] = useState(false);
    const { setMenuOpen } = useHamburgerContext();
    const { setSearchPannelOpen } = useSearchPanelContext();
    const { openModal } = useCartContext();

    useEffect(() => {
        const handleScroll = () => {
            if (window.scrollY > 90) {
                setNavbarFixed(true);
            } else {
                setNavbarFixed(false);
            }
        };

        window.addEventListener("scroll", handleScroll);
    }, []);

    return (
        <nav
            className={`${styles.navbar} ${
                navbarFixed !== false ? styles.fixed : ""
            }`}
        >
            <div className={styles.subcontainer}>
                <button
                    className={styles.hammenubtn}
                    onClick={() => setMenuOpen(true)}
                >
                    <div>
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                    <p>Menu</p>
                </button>
            </div>
            <div className={styles.subcontainer}>
                <Link className={styles.logo} to={"/"}>
                    PULL&BEAR
                </Link>
            </div>
            <div className={styles.subcontainer}>
                <div className={styles.utilscontainer}>
                    <button
                        className={styles.searchBtn}
                        onClick={() => setSearchPannelOpen(true)}
                    >
                        <i className="fa-solid fa-magnifying-glass"></i>
                        <p>Search</p>
                    </button>
                    <button
                        className={styles.mobileSearchBtn}
                        onClick={() => setSearchPannelOpen(true)}
                    >
                        <i className="fa-solid fa-magnifying-glass"></i>
                    </button>
                    <button className={styles.accountBtn}>
                        <i className="fa-solid fa-user"></i>
                    </button>
                    <button className={styles.cartBtn} onClick={() => openModal("cart")}>
                        <i className="fa-solid fa-cart-shopping"></i>
                    </button>
                </div>
            </div>
        </nav>
    );
}
