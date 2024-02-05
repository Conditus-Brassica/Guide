"use client"
import { useState } from "react";
import styles from "@/styles/round_button.module.css"

interface TheButtonInterface {
    image_path: string;
    type: string;
    mapData: any;
    functional: any;
    setTargetCats: any;
    targetCats: any;
    // setMapData: any;
};


const TheButton: React.FC<TheButtonInterface> = ({ image_path, type, mapData, functional, setTargetCats, targetCats }) => {
    const [buttonState, setButtonState] = useState(true);


    const handlerButtonClick = () => {
        setButtonState(pref => {
            pref = !pref
            return pref
        })

        if (functional == 'filter') {
            mapData.markers.forEach(function (drowedMarker: any) {
                if (drowedMarker.type == type) {
                    drowedMarker.setOpacity(buttonState ? 1 : 0)
                    // drowedMarker.getElement().style.pointerEvents = buttonState.isPressed? 'none': 'auto'; 
                };
            });
        }
        else {
            if (buttonState && !targetCats.includes(type)) {
                setTargetCats((prev: string[]) => {
                    console.log('push', type)
                    prev.push(type)
                    return prev
                })
            }
        }
    };

    return (
        <div className={styles.button} onClick={handlerButtonClick}>
            <div className={styles.content}>
                <img src={image_path} alt={type} />
                <span>{type}</span>
            </div>
        </div>
    );
};

export default TheButton