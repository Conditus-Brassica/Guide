import MapView, { PROVIDER_GOOGLE, Region } from "react-native-maps";
import { StyleSheet } from "react-native";
import { MapViewRoute } from "react-native-maps-routes";
import { useMapStore } from "@/hooks/useMapStore";
import React, { FC } from "react";

// A lot of test values to ensure everything works as it should
const origin = { latitude: 53.893009, longitude: 27.567444 };
const destination = { latitude: 53.771707, longitude: 25.567444 };

export const MapGuide: FC = () => {
  const mapInitialPosition = useMapStore((state) => state.initialPosition);
  return (
    <MapView
      style={styles.map}
      provider={PROVIDER_GOOGLE}
      initialRegion={mapInitialPosition}
    >
      <MapViewRoute
        origin={origin}
        destination={destination}
        apiKey={process.env.EXPO_PUBLIC_GOOGLE_MAPS_API_KEY ?? ""}
      />
    </MapView>
  );
};

const styles = StyleSheet.create({
  map: {
    width: "100%",
    height: "100%",
  },
});
