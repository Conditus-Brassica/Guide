import MapView, { Marker, PROVIDER_GOOGLE, Region } from "react-native-maps";
import { StyleSheet } from "react-native";
import { MapViewRoute } from "react-native-maps-routes";
import { useMapStore } from "@/hooks/useMapStore";
import React, { FC, useEffect, useState } from "react";
import * as Location from "expo-location";
import { landmarkInfo } from "@/types/landmarks-types";
import { Colors } from "@/constants/Colors";

type PropsType = {
	landmarks: landmarkInfo[] | null;
	mapPress: () => void;
};

export const MapGuide: FC<PropsType> = ({ landmarks, mapPress }) => {
	const [location, setLocation] = useState<Location.LocationObject | null>(
		null
	);
	const [errorMsg, setErrorMsg] = useState<string | null>(null);
	const [markers, setMarkers] = useState<landmarkInfo[] | null>(landmarks); //maybe only coords and name?

	const mapInitialPosition = useMapStore((state) => state.initialPosition);
	const routeCoords = useMapStore((state) => state.activeRoute);

	const setInitialPosition = useMapStore((state) => state.setInitialCoords);
	const setRouteCoords = useMapStore((state) => state.setActiveRoute);

	let text = "Waiting...";
	if (errorMsg) {
		text = errorMsg;
	} else if (location) {
		text = JSON.stringify(location);
	}

	useEffect(() => {
		if (landmarks && location) {
			setRouteCoords({
				origin: {
					latitude: location.coords.latitude,
					longitude: location.coords.longitude,
				},
				destination: {
					latitude: landmarks[0]._source.coordinates.latitude,
					longitude: landmarks[0]._source.coordinates.longitude,
				},
			});
		}
	}, [landmarks]);

	useEffect(() => {
		async function getCurrentLocation() {
			try {
				let { status } = await Location.requestForegroundPermissionsAsync();
				if (status !== "granted") {
					setErrorMsg("Permission to access location was denied");
					return;
				}

				let location = await Location.getCurrentPositionAsync({});
				setLocation(location);
				console.log(location.coords);
				setInitialPosition(location.coords);
			} catch (error) {
				alert(`Failed to get location:${error}`);
			}
		}

		getCurrentLocation();
	}, []);

	return (
		<MapView
			style={styles.map}
			provider={PROVIDER_GOOGLE}
			initialRegion={mapInitialPosition}
			showsUserLocation={true}
			showsCompass={false}
			showsMyLocationButton={false}
			onPress={mapPress}
		>
			{!!routeCoords && (
				<MapViewRoute
					origin={routeCoords.origin}
					destination={routeCoords.destination}
					apiKey={process.env.EXPO_PUBLIC_GOOGLE_MAPS_API_KEY ?? ""}
					strokeColor={Colors.standartAppColor}
				/>
			)}
			{!!markers &&
				markers.map((marker) => (
					<Marker id={marker._id} coordinate={marker._source.coordinates} />
				))}
		</MapView>
	);
};

const styles = StyleSheet.create({
	map: {
		width: "100%",
		height: "100%",
	},
});
