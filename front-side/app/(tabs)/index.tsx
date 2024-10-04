import React from "react";
import MapView, { PROVIDER_GOOGLE } from "react-native-maps";
import { StyleSheet, View } from "react-native";
import { MapViewRoute } from "react-native-maps-routes";
import Config from "react-native-config";

const initialPosition = {
  latitude: 53.893009,
  longitude: 27.567444,
  latitudeDelta: 0.5,
  longitudeDelta: 0.2,
};
const origin = { latitude: 37.3318456, longitude: -122.0296002 };
const destination = { latitude: 37.771707, longitude: -122.4053769 };
console.log(Config.GOOGLE_MAPS_API_KEY);
export default function App() {
  return (
    <View style={styles.container}>
      <MapView
        style={styles.map}
        provider={PROVIDER_GOOGLE}
        initialRegion={initialPosition}
      >
        <MapViewRoute
          origin={origin}
          destination={destination}
          apiKey={Config.GOOGLE_MAPS_API_KEY ?? ""}
        />
      </MapView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  map: {
    width: "100%",
    height: "100%",
  },
});
