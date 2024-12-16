import MapView, { LatLng, Marker, PROVIDER_GOOGLE } from "react-native-maps";
import { StyleSheet } from "react-native";
import { MapViewRoute } from "react-native-maps-routes";
import { useMapStore } from "@/hooks/useMapStore";
import React, { FC, useEffect, useState } from "react";

import { Colors } from "@/constants/Colors";
import { Recommendation } from "@/types/landmarks-types";

type PropsType = {
	landmarks: MarkerType[] | null;
	mapPress: () => void;

	recommendations: Recommendation[];
	setRecommendations: (recommendations: Recommendation[]) => void;
};

type MarkerType = {
	name: string;
	coordinates: LatLng;
};

export const MapGuide: FC<PropsType> = ({
	landmarks,
	mapPress,
	recommendations,
	setRecommendations,
}) => {
	const [markers, setMarkers] = useState<MarkerType[] | null>(landmarks);

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
						key={marker.name}
						title={marker.name}
						coordinate={marker.coordinates}
						onCalloutPress={() => {
							console.log("press");
							setRecommendations(
								recommendations?.filter((r) => r.name !== marker.name) ?? []
							);
						}}
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
