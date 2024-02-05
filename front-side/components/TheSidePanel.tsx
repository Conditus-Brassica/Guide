'use client'

import styles from "@/styles/sidepanel.module.css"
import TheRoundButton from "./TheRoundButton";
import { useEffect } from "react";
import { useState } from "react";


interface TheSidePanelInterface {
    setTargetCats: any;
    mapData: any;
    targetCats:any;
};



const getCategories = async function () {
    const response = await fetch(`http://0.0.0.0:4444/api/v1/map/categories`);
    const data: string[] = await response.json();
    const categories_dict: { [key: string]: string}  = {
        'Озёра': 'Rivers',
        'Историко-культурные ценности': 'Historical_and_cultural_values',
        'Природные места':'Natural_places',
        'Активный отдых': 'Leisure',
        'Мемориальные комплексы': 'Memorial_complexes',
        'Музеи':'Museums',
        'Театры':'Theatres',
        'Сады и парки':'Gardens_and_Parks',
    };
    
    var new_data: string[]=[] 
    data.forEach(element => {
        new_data.push(categories_dict[element])        
    });

    //     const data = [
//         'museum', 'restaurant', 'river'
//     ]

    return data
}


const TheSidePanel: React.FC<TheSidePanelInterface> =  ({ setTargetCats, mapData, targetCats }) => {

    const [categories, setCategories] = useState<string[]>([]);

    useEffect(() => {
      const fetchData = async () => {
        const data = await getCategories();
        setCategories(data);
      };
  
      fetchData();
    }, []);
    

    return (
        <div className={styles.panel}>
            <div className={styles.search}>search</div>
            <div className={styles.buttons}>
                {categories.map((value: string, index: number) => (
                    <div key={index}>
                        <TheRoundButton targetCats={targetCats} type={value}  image_path={`/${value}.svg`} functional='filter' mapData={mapData} setTargetCats={setTargetCats}/>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default TheSidePanel;