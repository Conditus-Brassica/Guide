import Link from "next/link";
import styles from "@/styles/header.module.css"

const TheHeader = () =>{
return(
 <header className={styles.header}>
  <ul className={styles.menu}>
    <li className={styles.menu_item}><Link href="/route">Маршруты</Link></li>
    <li className={styles.menu_item}><Link href="/guide">Гиды</Link></li>
    <li className={styles.menu_item}><Link href="/excursion">Экскурсии</Link></li>
  </ul>
 </header>
);
} ;

export {TheHeader}