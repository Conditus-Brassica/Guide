import sidepanel_style from "@/styles/sidepanel.module.css"
import TheButton from "./TheButton";
import { useEffect } from "react";
import CustomMarker from "./TheMap"
import style from "@/styles/route_panel.module.css"

interface TheRoutePanel {
    setRoute: any;
    route: any;
    mapData: any;
};

const TheRoutePanel: React.FC<TheRoutePanel> = ({ setRoute, route, mapData }) => {

    const finishRoute = function () {
        setRoute((pref: boolean) => {
            pref = false
            return pref
        })
    }


    return (
        <>
            {<div style={{ display: route ? 'block' : 'none' }}>
                <div className={sidepanel_style.panel}>
                    <div className={style.name}>
                       <h3>Маршрут</h3>
                    </div>
                   <div>
                   {mapData.markers.map((value: typeof CustomMarker, index:number) => (
                        <div className={style.row} key={index}>
                            <div className={style.number}>
                                <span>{index + 1}</span>
                            </div>
                            <p key={index +1}>{value.name}</p>
                        </div>
                    ))}
                    </div>
                    <TheButton title="Закончить маршрут!" func={finishRoute} />
                </div>
            </div>
            }
        </>
    );
};

export default TheRoutePanel