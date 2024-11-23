import MapView, { PROVIDER_GOOGLE, Region } from "react-native-maps";
import { StyleSheet } from "react-native";
import { MapViewRoute } from "react-native-maps-routes";
import { useMapStore } from "@/hooks/useMapStore";
import React, { FC } from "react";

export const MapGuide: FC = () => {
	const mapInitialPosition = useMapStore((state) => state.initialPosition);
	const routeCoords = useMapStore((state) => state.activeRoute);
	return (
		<MapView
			style={styles.map}
			provider={PROVIDER_GOOGLE}
			initialRegion={mapInitialPosition}
		>
			{routeCoords && (
				<MapViewRoute
					origin={routeCoords.origin}
					destination={routeCoords.destination}
					apiKey={process.env.EXPO_PUBLIC_GOOGLE_MAPS_API_KEY ?? ""}
				/>
			)}
		</MapView>
	);
};

const styles = StyleSheet.create({
	map: {
		width: "100%",
		height: "100%",
	},
});
