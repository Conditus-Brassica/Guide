'use client'

import { useEffect } from 'react';
import L, { LatLng, latLng } from 'leaflet';
import styles from '@/styles/map.module.css'
import { LatLngExpression } from 'leaflet';
import { Marker } from 'react-leaflet';


interface TheMapInterface {
  setMapData: any;
  markerState: any;
  setMarkerState: any;
  setLandmark: any;
  route: any;
  targetCats: any;
  setTargetCats: any;
};


class CustomMarker extends L.Marker {
  type: string;
  name: string;
  constructor(latlng: LatLngExpression, options: any) {
    super(latlng, options);
    this.type = options.type || 'none';
    this.name = options.name || 'none';
  }
};


const TheMap: React.FC<TheMapInterface> = ({ setMapData, markerState, setMarkerState, setLandmark, route, targetCats, setTargetCats }) => {
  useEffect(() => {
    const map = L.map('map').setView([51.505, -0.09], 13);
    var BelarusGeoJSON: any = {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "properties": {},
          "geometry": {
            "type": "Polygon",
            "coordinates": [
              [
                [23.5149129, 53.9760145],
                [23.9104208, 53.0285526],
                [23.1523641, 52.2754422],
                [23.5368856, 51.5229876],
                [23.9323934, 51.5844674],
                [25.5803426, 51.9109574],
                [27.6457723, 51.4614248],
                [30.5791219, 51.2693639],
                [30.5901083, 51.611765],
                [30.9306844, 52.0800705],
                [31.7986043, 52.1205627],
                [31.3921102, 53.1934206],
                [32.1281942, 53.0285526],
                [32.7104696, 53.3117344],
                [32.7104696, 53.4689775],
                [31.150411, 54.648944],
                [30.9746297, 55.5850737],
                [30.348409, 55.8449979],
                [28.1291708, 56.152181],
                [26.6570028, 55.6842964],
                [25.8110555, 54.9339821],
                [25.5363973, 54.3298737],
                [23.5149129, 53.9760145]
              ]
            ]
          }
        }]
    };

    var BelarusLayer: any = L.geoJSON(BelarusGeoJSON);
    map.setView(BelarusLayer.getBounds().getCenter(), 10);
    map.setMaxBounds(BelarusLayer.getBounds());
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    }).addTo(map);

    const icons: { [key: string]: L.Icon } = {
      "none":
        L.icon({
          iconUrl: 'green_icon.svg',
          iconSize: [30, 30],
        }),
      "start":
        L.icon({
          iconUrl: 'self.png',
          iconSize: [30, 30],
        })
    };

    setTargetCats((prev: never[])=> {
      prev=[]
      return prev
  })

    const onMarkerClick = function (e: L.LeafletMouseEvent) {
      if (markerState.targetMarker == e.target) {
        setLandmark((pref: boolean) => {
          pref = !pref
          return pref
        })
      }
      else {
        setLandmark((pref: boolean) => {
          pref = true
          return pref
        })
      }
      setMarkerState((pref: { targetMarker: any; }) => {
        pref.targetMarker = e.target
        return pref
      })
    };

    var drawnedMarkers: Array<CustomMarker> = [];

    const getPoints = async function (tl: any, br: any) {
      try {
        const response = await fetch(`http://0.0.0.0:4444/api/v1/sector/points?tl_lat=${tl[0]}&tl_lng=${tl[1]}&br_lat=${br[0]}&br_lng=${br[1]}`);
        const data = await response.json();
        console.log(data);
//         const data = {
//           points: [{
//             name: "name",
//             lat: 54.098865472796994,
//             lng: 26.661071777343754,
//             type: "museum"
//           }, {
//             name: "name1",
//             lat: 54.098865472796994,
//             lng: 26.761071777343754,
//             type: "restaurant"
//           }, {
//             name: "name2",
//             lat: 54.098865472796994,
//             lng: 26.861071777343754,
//             type: "river"
//           }]
//         }

        data.points.forEach(function (markerCoords: any) {
          const isDuplicate = drawnedMarkers.some(drawnedMarker => drawnedMarker.getLatLng().lat === markerCoords.lat && drawnedMarker.getLatLng().lng === markerCoords.lng);

          if (!isDuplicate) {
            var marker = new CustomMarker([markerCoords.lat, markerCoords.lng], { icon: icons[markerCoords.type], type: markerCoords.type, name: markerCoords.name });
            marker.addTo(map);
            marker.bindPopup(markerCoords.name);
            drawnedMarkers.push(marker);
            marker.on('click', onMarkerClick);
          };
        });

        var updatedMapData = { markers: drawnedMarkers };
        setMapData(updatedMapData);

      } catch (error) {
        alert("Не удалось загрузить достпуные достопримечательности. Проверьте соединение с интернетом!");
        console.log(error)
      }
    };

    async function getRoute(start: any, finish: any, cat: any) {
      try {
        const response = await fetch(`http://0.0.0.0:4444/api/v1/map/route?start=${start}&finish=${finish}&catigories=${cat}`);
        var data = await response.json();
        console.log(cat)
//         const data = {
//           route: [
//             [54.098865472796994, 26.661071777343754,],
//             [54.098865472796994,
//               26.761071777343754,],
//               [54.098865472796994,
//                 26.861071777343754,]
//           ],
//           points: [
//             {
//               name: 'first',
//               latlng: [54.098865472796994, 26.661071777343754,]
//             },
//             {
//               name: 'first',
//               latlng: [54.098865472796994,
//                 26.761071777343754,]
//             },
//             {
//               name: 'first',
//               latlng: [54.098865472796994,
//                 26.861071777343754,]
//             }
//           ]
//         };

        const latLngs = data.route.map((coords: number[]) => L.latLng(coords[0], coords[1]));
        const route = L.polyline(latLngs).addTo(map);

        data.points.forEach((point: { latlng: L.LatLngExpression; name: ((layer: L.Layer) => L.Content) | L.Content | L.Popup; }) => {
          const marker = new CustomMarker(point.latlng, { icon: icons['none'], type: 'none', name: point.name}).addTo(map);
          marker.bindPopup(point.name);
          drawnedMarkers.push(marker);
        });
        var updatedMapData = { markers: drawnedMarkers };
        
        setMapData(updatedMapData);
        console.log(updatedMapData)
        const markersLayer = L.layerGroup(drawnedMarkers);
        map.addLayer(route);
        map.addLayer(markersLayer);

        console.log(updatedMapData)
      } catch (error) {
        alert("Что-то пошло не так! Проверьте соединение с интернетом!");
      }
    };

    const onMapMoveEnd = function () {
      var left_top = [map.getBounds().getNorthWest().lat, map.getBounds().getNorthWest().lng]
      var right_bottom = [map.getBounds().getSouthEast().lat, map.getBounds().getSouthEast().lng]
      getPoints(left_top, right_bottom)
      console.log('перемещение отрабатывает')
    };

    if (route == true) {
      map.off('moveend', onMapMoveEnd);
      console.log('moveend размонтирована')

      const onSuccess = function (position: GeolocationPosition) {
        setMapData((pref: { markers: any[]; }) => {
          pref.markers.forEach(marker => {
            marker.removeFrom(map);
          });
          return pref;
        });

        var start: LatLngExpression = [position.coords.latitude, position.coords.longitude]
        var finish = [markerState.targetMarker._latlng.lat, markerState.targetMarker._latlng.lng] 
        console.log('маршрут от', start, finish)
        getRoute(start, finish, targetCats)
        var marker = new CustomMarker(start, { icon: icons['start'], type: 'start' });
        marker.addTo(map);
        console.log(`Ваши координаты: ${start}`);
      }

      const onError = function (error: GeolocationPositionError) {
        console.log(`Ошибка при получении местоположения: ${error.message}`);
      }

      if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(onSuccess, onError);
      } else {
        alert("Geolocation не поддерживается в вашем браузере");
      }
    }
    else {
      console.log('moveend вмонтирована')
      onMapMoveEnd();
      map.on('moveend', onMapMoveEnd);
    }

    return () => {
      map.remove(); // Очистка карты при размонтировании компонента
    };
  }, [route]);


  return (<div id="map" className={styles.map}>
  </div>);
};

export default TheMap