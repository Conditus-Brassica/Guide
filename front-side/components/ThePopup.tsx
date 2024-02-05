import TheButton from "./TheButton";
import style from "@/styles/popup.module.css"
import TheRoundButton from "./TheRoundButton"
import { useState, useEffect } from "react";

interface ThePopup {
    setLandmark: any;
    popup: any;
    setRoute: any;
    setPopup: any;
    mapData: any;
    setTargetCats:any;
    targetCats:any;
}

const getCategories = async function () {
    const response = await fetch(`http://0.0.0.0:4444/api/v1/map/categories`);
    const data: string[] = await response.json();
    
    return data
}

const ThePopup: React.FC<ThePopup> = ({ setLandmark, popup, setRoute, setPopup, mapData, setTargetCats, targetCats }) => {
    const buildARoute = function () {
        setRoute((pref: boolean) => {
            console.log('route=', pref)
            pref = true
            return pref
        })
        setLandmark(false)
        setPopup(false)
    }

    const [categories, setCategories] = useState<string[]>([]);

    useEffect(() => {
      const fetchData = async () => {
        const data = await getCategories();
        setCategories(data);
      };
  
      fetchData();
    }, []);

    return (<>
        {<div style={{ display: popup ? 'block' : 'none' }} className={style.popup}>
            <div className={style.content}>
                <div className={style.cat}>
                    {categories.map((value: string, index: number) => (

                        <div key={index}>
                            <TheRoundButton targetCats={targetCats} type={value} image_path={`/${value}.svg`} functional='fetch' mapData={mapData} setTargetCats={setTargetCats}/>
                        </div>

                    ))}
                </div>
                <TheButton title="Составить маршрут!" func={buildARoute} />
            </div>
        </div>}
    </>
    )
}

export default ThePopup