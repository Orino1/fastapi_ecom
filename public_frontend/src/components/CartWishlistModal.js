import styles from "../assets/styles/componenets/CartWishlistModal.module.css";
import { useCartContext } from "../contexts/CartContext";
import ProductCardInCart from "./ProductCardInCart";
import ProductCard from "./ProductCard";

export default function CartWishlistModal() {
    const { closeModal, openModal, currentView, cartItems, wishlistItems } =
        useCartContext();

    const renderContent = () => {
        if (currentView === "cart") {
            // show cart
            if (cartItems.length === 0) {
                // cart empty
                return <CartEmpty />;
            } else {
                // items in cart
                return <CartWithItems />;
            }
        } else {
            // show wishlist
            if (cartItems.length === 0) {
                // wishlist empty
                return <WishListEmpty />;
            } else {
                // items in wishlist
                return <WishlistWithItems />;
            }
        }
    };

    return (
        <div className={styles.background} onClick={closeModal}>
            <div className={styles.main} onClick={(e) => e.stopPropagation()}>
                <header>
                    <button
                        onClick={() => openModal("cart")}
                        className={
                            currentView === "cart" ? styles.selected : ""
                        }
                    >
                        Shopping bag({cartItems.length})
                    </button>
                    <button
                        onClick={() => openModal("wish")}
                        className={
                            currentView === "wish" ? styles.selected : ""
                        }
                    >
                        Wishlist({wishlistItems.length})
                    </button>
                    <button onClick={closeModal}>
                        <i className="fa-solid fa-x"></i>
                    </button>
                </header>
                <div className={styles.content}>{renderContent()}</div>
            </div>
        </div>
    );
}

function CartEmpty() {
    return (
        <div className={styles.cartEmpty}>
            <header>
                <h1>Your shopping basket is empty</h1>
                <p>Why not fill it with some of our suggestions?</p>
            </header>
            <hr></hr>
            <div className={styles.prodctsContainer}>
                <h1>Suggested for you</h1>
                <div>
                    <ProductCard />
                    <ProductCard />
                    <ProductCard />
                    <ProductCard />
                    <ProductCard />
                </div>
            </div>
        </div>
    );
}

function WishListEmpty() {
    return (
        <div className={styles.cartEmpty}>
            <header>
                <h1>Your wishlist is empty</h1>
                <p>Why not fill it with some of our suggestions?</p>
            </header>
            <hr></hr>
            <div className={styles.prodctsContainer}>
                <h1>Suggested for you</h1>
                <div>
                    <ProductCard />
                    <ProductCard />
                    <ProductCard />
                    <ProductCard />
                    <ProductCard />
                </div>
            </div>
        </div>
    );
}

function CartWithItems() {
    return (
        <div className={styles.cartWithItems}>
            <div className={styles.productsContainer}>
                <ProductCardInCart />
                <ProductCardInCart />
                <ProductCardInCart />
                <ProductCardInCart />
            </div>
            <hr></hr>
            <div className={styles.suggestedContainer}>
                <ProductCard />
                <ProductCard />
                <ProductCard />
                <ProductCard />
                <ProductCard />
            </div>
        </div>
    );
}

function WishlistWithItems() {
    return (
        <div className={styles.wishlistWithItems}>
            <div className={styles.productsContainer}>
                <ProductCard />
                <ProductCard />
                <ProductCard />
                <ProductCard />
            </div>
            <hr></hr>
            <div className={styles.suggestedContainer}>
                <ProductCard />
                <ProductCard />
                <ProductCard />
                <ProductCard />
                <ProductCard />
            </div>
        </div>
    );
}
