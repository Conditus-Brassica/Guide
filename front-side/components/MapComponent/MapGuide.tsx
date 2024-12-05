import MapView, { Marker, PROVIDER_GOOGLE, Region } from "react-native-maps";
import { ActivityIndicator, Alert, StyleSheet, View } from "react-native";
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
	const [markers, setMarkers] = useState<landmarkInfo[] | null>(landmarks);
	const [loading, setLoading] = useState(false);

	const mapInitialPosition = useMapStore((state) => state.initialPosition);
	const routeCoords = useMapStore((state) => state.activeRoute);

	const setInitialPosition = useMapStore((state) => state.setInitialCoords);
	const setRouteCoords = useMapStore((state) => state.setActiveRoute);

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
			setMarkers(landmarks);
		}
	}, [landmarks]);

	useEffect(() => {
		async function getCurrentLocation() {
			try {
				let { status } = await Location.requestForegroundPermissionsAsync();
				if (status !== "granted") {
					Alert.alert("Error", "Permission to access location was denied");
					return;
				}

				let location = await Location.getCurrentPositionAsync({});
				setLocation(location);
				console.log(location.coords);
				setInitialPosition(location.coords);
			} catch (error) {
				alert(`Failed to get location:${error}`);
			} finally {
				setLoading(false);
			}
		}

		getCurrentLocation();
	}, []);

	if (loading) {
		// Show a loader while location is being fetched
		return (
			<View style={styles.loaderContainer}>
				<ActivityIndicator size="large" color={Colors.standartAppColor} />
			</View>
		);
	}

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
					<Marker
						key={marker._id}
						title={marker._source.name}
						coordinate={marker._source.coordinates}
					/>
				))}
		</MapView>
	);
};

const styles = StyleSheet.create({
	map: {
		width: "100%",
		height: "100%",
	},
	loaderContainer: {
		flex: 1,
		justifyContent: "center",
		alignItems: "center",
	},
});
