import styles from "../assets/styles/componenets/Footer.module.css";
import { Link } from "react-router-dom";
import adnroidImg from "../assets/images/android.png";
import iosImg from "../assets/images/ios.png";
import mastercard from "../assets/images/MasterCard.svg";
import cod from "../assets/images/COD.svg";
import visa from "../assets/images/VISA.svg";

export default function Footer() {
    return (
        <footer className={styles.container}>
            <div className={styles.section}>
                <h1>Help</h1>
                <div>
                    <Link>Frequently asked questions</Link>
                    <Link>Processing a return</Link>
                </div>
            </div>
            <div className={styles.section}>
                <h1>Company</h1>
                <div>
                    <Link>About us</Link>
                    <Link>Work with us</Link>
                </div>
            </div>
            <div className={styles.section}>
                <div className={styles.subsection}>
                    <h1>Our app</h1>
                    <div>
                        <a
                            href="http://gooel.com"
                            target="_blank"
                            rel="noreferrer"
                        >
                            <img
                                src={adnroidImg}
                                alt="android application"
                            ></img>
                        </a>
                        <a
                            href="http://gooel.com"
                            target="_blank"
                            rel="noreferrer"
                        >
                            <img src={iosImg} alt="ios application"></img>
                        </a>
                    </div>
                </div>
                <div className={styles.subsection}>
                    <h1>Means of payment</h1>
                    <div>
                        <img src={mastercard} alt="master card"></img>
                        <img src={visa} alt="cisa card"></img>
                        <img src={cod} alt="cash on delivery"></img>
                    </div>
                </div>
                <div className={styles.subsection}>
                    <h1>Follow us!</h1>
                    <div>
                        <a
                            href="http://gooel.com"
                            target="_blank"
                            rel="noreferrer"
                        >
                            <i className="fa-brands fa-instagram"></i>
                        </a>
                        <a
                            href="http://gooel.com"
                            target="_blank"
                            rel="noreferrer"
                        >
                            <i className="fa-brands fa-facebook-f"></i>
                        </a>
                        <a
                            href="http://gooel.com"
                            target="_blank"
                            rel="noreferrer"
                        >
                            <i className="fa-solid fa-x"></i>
                        </a>
                        <a
                            href="http://gooel.com"
                            target="_blank"
                            rel="noreferrer"
                        >
                            <i className="fa-brands fa-pinterest-p"></i>
                        </a>
                        <a
                            href="http://gooel.com"
                            target="_blank"
                            rel="noreferrer"
                        >
                           <i className="fa-brands fa-youtube"></i>
                        </a>
                        <a
                            href="http://gooel.com"
                            target="_blank"
                            rel="noreferrer"
                        >
                           <i className="fa-brands fa-tiktok"></i>
                        </a>
                    </div>
                </div>
            </div>
        </footer>
    );
}
