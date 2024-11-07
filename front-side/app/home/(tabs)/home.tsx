import React from "react";
import { StyleSheet, View } from "react-native";
import { MapGuide } from "@/components/MapComponent/MapGuide";

export default function App() {
	return (
		<View style={styles.container}>
			<MapGuide />
		</View>
	);
}

const styles = StyleSheet.create({
	container: {
		flex: 1,
	},
});
