"use client"
import styles from "@/styles/button.module.css"
import { useRouter } from "next/navigation";

interface TheButtonInterface{
    title: string;
    func: () => void;
};



const TheButton: React.FC<TheButtonInterface> = ({title, func}) => {
    const router = useRouter(); 

    return(
    <div className={styles.button} onClick={func}>
        <span className={styles.title}>{title}</span>
    </div>
);
};

export default TheButton;