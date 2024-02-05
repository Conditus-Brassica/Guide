import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import { GeoJsonObject } from 'geojson';

const TheDynamicMap = () =>{

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
    
      const center: any = [53.5, 27];
      const zoom = 7;
    
      return (
        <MapContainer center={center} zoom={zoom} style={{ height: '400px', width: '100%' }}>
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution="Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors" />
          <GeoJSON data={BelarusGeoJSON} />
        </MapContainer>
        )
}

export default TheDynamicMap;