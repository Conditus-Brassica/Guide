## Технологии
- [ORSM](https://github.com/Project-OSRM/osrm-backend?tab=readme-ov-file)

## Установка 
Установите карты Беларуси:
```sh
$ wget http://download.geofabrik.de/europe/belarus-latest.osm.pbf
```

Установка всех нужных файлов:
```sh
$ sudo docker run -t -v "${PWD}:/data" ghcr.io/project-osrm/osrm-backend osrm-extract -p /opt/car.lua /data/belarus-latest.osm.pbf || echo "osrm-extract failed"

$ sudo docker run -t -v "${PWD}:/data" ghcr.io/project-osrm/osrm-backend osrm-partition /data/belarus-latest.osrm || echo "osrm-partition failed"

$ sudo docker run -t -v "${PWD}:/data" ghcr.io/project-osrm/osrm-backend osrm-customize /data/belarus-latest.osrm || echo "osrm-customize failed"
```

## Запуск
Запуск сервера:
```sh
$ sudo docker run -t -i -p 5000:5000 -v "${PWD}:/data" ghcr.io/project-osrm/osrm-backend osrm-routed --algorithm mld /data/belarus-latest.osrm
```

## Пример работы 
```python

points = [[53.864888, 27.486680], [53.911907, 27.596647]]
coordinates = ';'.join([f"{point[1]},{point[0]}" for point in points])
url = f"http://127.0.0.1:5000/route/v1/driving/{coordinates}?steps=true&geometries=geojson&overview=full"
response = requests.get(url)
if response.status_code == 200:
    json_data = response.json()
    print(json_data)

```
steps=true - получение пошаговой инструкции, возможно пока не надо 