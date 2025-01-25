import styles from "../assets/styles/componenets/SearchPanel.module.css";
import { Link } from "react-router-dom";
import { useState } from "react";
import { useSearchPanelContext } from "../contexts/SearchPanelContext";
import ProductCard from "./ProductCard";

export default function SearchPanel() {
    const {setSearchPannelOpen} = useSearchPanelContext();
    const [searcQuery, setSearchQuery] = useState("");

    return (
        <div className={styles.main}>
            <div className={styles.uppersection}>
                <header>
                    <div>
                        <h1 className={styles.selected}>Woman</h1>
                        <h1>Man</h1>
                    </div>
                    <div>
                        <Link>PULL&BEAR</Link>
                    </div>
                    <div>
                        <button onClick={() => setSearchPannelOpen(false)}>
                            <i className="fa-solid fa-x"></i>
                        </button>
                    </div>
                </header>
                <div>
                    <i className="fa-solid fa-magnifying-glass"></i>
                    <input
                        value={searcQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        placeholder="What are you looking for?"
                    ></input>
                    <button onClick={() => setSearchQuery("")}>
                        <i className="fa-solid fa-x"></i>
                    </button>
                </div>
                <hr></hr>
            </div>
            <div className={styles.lowersection}>
                <h1>Suggested for you</h1>
                <div className={styles.productsContainer}>
                    <ProductCard/>
                    <ProductCard/>
                    <ProductCard/>
                    <ProductCard/>
                    <ProductCard/>
                    <ProductCard/>
                    <ProductCard/>
                    <ProductCard/>
                    <ProductCard/>
                    <ProductCard/>
                    <ProductCard/>
                    <ProductCard/>
                    <ProductCard/>
                    <ProductCard/>
                    <ProductCard/>
                    <ProductCard/>
                    <ProductCard/>
                </div>
            </div>
        </div>
    );
}
