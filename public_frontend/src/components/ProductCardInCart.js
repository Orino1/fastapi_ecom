import styles from "../assets/styles/componenets/ProductCardInCart.module.css";
import { Link } from "react-router-dom";

export default function ProductCardInCart() {
    return (
        <div className={styles.container}>
            <img alt="tumbnail"></img>
            <div>
                <Link>Striped open knit jumper</Link>
                <h4>169.00 MAD</h4>
                <div>
                    <span>1 item</span>
                    <span>M</span>
                    <span>Green</span>
                </div>
                <div>
                    <button className={styles.active}>
                        <i className={"fa-regular fa-heart"}></i>
                    </button>
                    <button>
                        <i className="fa-solid fa-trash"></i>
                    </button>
                </div>
            </div>
        </div>
    );
}
