import styles from "../assets/styles/componenets/HamburgerMenu.module.css";
import { useHamburgerContext } from "../contexts/HamburgerContext";
import { Link } from "react-router-dom";

export default function HamburgerMenu() {
    const { setMenuOpen } = useHamburgerContext();

    return (
        <div className={styles.background} onClick={() => setMenuOpen(false)}>
            <div className={styles.main} onClick={(e) => e.stopPropagation()}>
                <header>
                    <h1 className={styles.selected}>WOMAN</h1>
                    <h1>MAN</h1>
                    <button onClick={() => setMenuOpen(false)}>x</button>
                </header>
                <div
                    className={styles.content}
                    onClick={() => setMenuOpen(false)}
                >
                    <Link>Shoes</Link>
                    <Link className={styles.selected}>T-Shirts</Link>
                    <Link>Jackets</Link>
                    <Link>Pants</Link>
                    <Link>Dresses</Link>
                </div>
            </div>
        </div>
    );
}
