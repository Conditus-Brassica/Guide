import MapView, { Marker, PROVIDER_GOOGLE, Region } from "react-native-maps";
import { ActivityIndicator, Alert, StyleSheet, View } from "react-native";
import { MapViewRoute } from "react-native-maps-routes";
import { useMapStore } from "@/hooks/useMapStore";
import React, { FC, useEffect, useState } from "react";

import { landmarkInfo } from "@/types/landmarks-types";
import { Colors } from "@/constants/Colors";

type PropsType = {
	landmarks: landmarkInfo[] | null;
	mapPress: () => void;
};

export const MapGuide: FC<PropsType> = ({ landmarks, mapPress }) => {
	const [markers, setMarkers] = useState<landmarkInfo[] | null>(landmarks);

	const mapInitialPosition = useMapStore((state) => state.initialPosition);
	const routeCoords = useMapStore((state) => state.activeRoute);

	useEffect(() => {
		setMarkers(landmarks);
	}, [landmarks]);

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
			{routeCoords?.origin && routeCoords?.destination && (
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
