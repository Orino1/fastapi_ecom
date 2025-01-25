import styles from "../assets/styles/componenets/HeaderAnnoucment.module.css";
import { useHeaderAnnoucmetContext } from "../contexts/HeaderAnnoucmentContext";

export default function HeaderAnnoucment() {
    const { announcement, setAnnouncement } = useHeaderAnnoucmetContext();

    return (
        <div className={styles.main}>
            <p>{announcement}</p>
            <button onClick={() => setAnnouncement(null)}>X</button>
        </div>
    );
}
