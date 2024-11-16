import React from "react";
import { StyleSheet, View } from "react-native";
import { MapGuide } from "@/components/MapComponent/MapGuide";
//@ts-ignore
import { SearchBox } from "@appbaseio/react-native-searchbox";

export default function App() {
	return (
		<View style={styles.container}>
			<SearchBox></SearchBox>
			<MapGuide />
		</View>
	);
}

const styles = StyleSheet.create({
	container: {
		flex: 1,
	},
});
