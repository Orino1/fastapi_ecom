import "../assets/styles/pages/globalstyles.css";
import MainLayout from "../layouts/MainLayout";
import styles from "../assets/styles/pages/Home.module.css";
import ProductCard from "../components/ProductCard";

export default function Home() {
    return (
        <MainLayout>
            <div className="container">
                <div className={styles.productsContainer}>
                    <ProductCard />
                    <ProductCard />
                    <ProductCard />
                    <ProductCard />
                    <ProductCard />
                    <ProductCard />
                    <ProductCard />
                    <ProductCard />
                    <ProductCard />
                    <ProductCard />
                    <ProductCard />
                    <ProductCard />
                    <ProductCard />
                </div>
            </div>
        </MainLayout>
    );
}
