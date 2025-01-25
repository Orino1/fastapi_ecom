import styles from "../assets/styles/componenets/ProductCard.module.css";
import { Link } from "react-router-dom";
import { useState } from "react";

export default function ProductCard() {
    const [actionsShown, setActionsShown] = useState(false);
    const [sizesShown, setSizesShown] = useState(false);

    const handleMouseOverProduct = () => {
        setActionsShown(true);
    };

    const handleMouseOutOfProduct = () => {
        setActionsShown(false);
    };

    const handleMouseOverDropdown = () => {
        setSizesShown(true);
    };

    const handleMouseOutOdDropdown = () => {
        setSizesShown(false);
    };

    return (
        <div
            className={styles.container}
            onMouseEnter={handleMouseOverProduct}
            onMouseLeave={handleMouseOutOfProduct}
        >
            <div className={styles.subContainer}>
                <div className={styles.upperSection}>
                    <Link>
                        <img alt="tumbnail"></img>
                    </Link>
                    <div className={styles.promotionContainer}>
                        <div>-21%</div>
                        <div>ONLINE EXCLUSIVE</div>
                    </div>
                    <div
                        className={`${styles.actions} ${
                            actionsShown && styles.active
                        }`}
                        onClick={(e) => e.stopPropagation()}
                    >
                        <div
                            className={`${styles.sizeDropdown} ${
                                sizesShown && styles.active
                            }`}
                            onMouseEnter={handleMouseOverDropdown}
                            onMouseLeave={handleMouseOutOdDropdown}
                        >
                            <p className={styles.sizeHolder}>select</p>
                            <div className={styles.sizes}>
                                <div className={styles.size}>XS</div>
                                <div className={styles.size}>S</div>
                                <div className={styles.size}>M</div>
                                <div className={styles.size}>L</div>
                            </div>
                        </div>
                        <button>Add</button>
                    </div>
                </div>
                <div className={styles.lowerSection}>
                    <h1>Basic high neck jumper</h1>
                    <p className={`${styles.price} ${styles.discounted}`}>
                        169.00 MAD <span>650 MAD</span>
                    </p>
                    <p className={`${styles.colorsCount} ${actionsShown && styles.hide}`}>4 Colours</p>
                    <div className={`${styles.colorsContainer} ${actionsShown && styles.visible}`}>
                        <div className={styles.selected}>
                            <label>red</label>
                        </div>
                        <div>
                            <label>white</label>
                        </div>
                        <div>
                            <label>black</label>
                        </div>
                        <div>
                            <label>green</label>
                        </div>
                    </div>
                    <button className={styles.wishBtn}>
                        <i className="fa-regular fa-heart"></i>
                    </button>
                </div>
            </div>
        </div>
    );
}
