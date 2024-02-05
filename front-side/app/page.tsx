"use client"
import Head from "next/head";
import styles from "@/styles/main_page.module.css";
import Link from "next/link";
import button_styles from "@/styles/button.module.css"

export default function Home() {
  
  return (
    <>
      <Head>
        <title>Главная страница</title>
        <meta name="description" content="Главная страница сайта всевозможных генераторов для настольной игры D&D." />
        <meta name="keywords" content="" />
      </Head>
      <main className={styles.main_page}>
        <div className={styles.welcome_block}>
          <h1>✈TRAVELER.AI</h1>
          <h3>Ваш персональный гид по достопримечательностям Беларуси</h3>
          {/* <TheButton title={'Поехали!'} func={() => Routing('/map_route')}/> */}
          <Link className={button_styles.button} href={'/map_route'}>Поехали</Link>
        </div>
      </main>
    </>
  )
}