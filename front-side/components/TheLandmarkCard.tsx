import style from "@/styles/landmark_card.module.css"
import { useState } from "react";
import sidepanel_style from "@/styles/sidepanel.module.css"
import TheButton from "./TheButton";
import buildARoute from "./ThePopup"

interface TheLandmarkCard {
    setLandmark: any;
    landmark: any;
    setPopup: any;
    setRoute:any;
}


const TheLandmarkCard: React.FC<TheLandmarkCard> = ({ landmark, setPopup, setLandmark, setRoute }) => {
    const buildARoute = function () {
        setRoute((pref: boolean) => {
            console.log('route=', pref)
            pref = true
            return pref
        })
        setLandmark(false)
    }

    const callPopup = function () {
        if(isChecked){
            setPopup((pref: boolean) => {
                pref = true
                console.log(pref)
                return pref
            })
        }
        else{
            buildARoute()
        }
    }
    const [isChecked, setIsChecked] = useState(false);

    const handleCheckboxChange = () => {
        setIsChecked((pref: boolean) => {
            pref = !pref
            return pref
        });
    };
    return (<>
        {<div style={{ display: landmark ? 'block' : 'none' }}>
            <div className={sidepanel_style.panel}>
                <div className={style.image}>
                    <img src="" alt="" />
                </div>
                <div className={style.name}>
                    <h3></h3>
                </div>
                <div className={style.description}>
                    <p></p>
                </div>
                <div>
                    <label>
                        <input
                            type="checkbox"
                            checked={isChecked}
                            onChange={handleCheckboxChange}
                        />
                        Рекомендовать достопримечательности
                    </label>
                </div>
                <TheButton title="Построить маршрут!" func={callPopup} />
            </div>
        </div>
        }
    </>
    )
}

export default TheLandmarkCard