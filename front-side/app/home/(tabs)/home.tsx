import React, { useState } from "react";
import {
	FlatList,
	StyleSheet,
	TextInput,
	View,
	Text,
	TouchableOpacity,
	Keyboard,
	KeyboardAvoidingView,
} from "react-native";
import { MapGuide } from "@/components/MapComponent/MapGuide";
import axios from "axios";
import { ELASTIC_URL } from "@/constants/request-api-constants";
import { Colors } from "@/constants/Colors";
import { setStatusBarHidden } from "expo-status-bar";
import { landmarkInfo } from "@/types/landmarks-types";
import { useDebouncedCallback } from "use-debounce";

const Item = ({
	item,
	onPress,
}: {
	item: landmarkInfo;
	onPress: (item: landmarkInfo) => void;
}) => (
	<TouchableOpacity
		style={styles.resultText}
		onPress={() => {
			onPress(item);
			Keyboard.dismiss();
		}}
	>
		<Text>{item._source.name}</Text>
	</TouchableOpacity>
);

export default function App() {
	const [results, setResults] = useState<landmarkInfo[]>([]);
	const [activeLandmarks, setActiveLandmarks] = useState<landmarkInfo[]>([]);
	const [query, setQuery] = useState("");
	setStatusBarHidden(false);

	const mapPress = () => {
		console.log("wow!");
		setResults([]);
		Keyboard.dismiss();
	};

	const onLandmarkPress = (item: landmarkInfo) => {
		setActiveLandmarks([item]);
		setQuery("");
		setResults([]);
	};

	const performSearch = useDebouncedCallback(async (searchQuery: string) => {
		try {
			const response = await axios.post(
				`${ELASTIC_URL}/landmarks_index/_search`,
				{
					size: 5,
					query: {
						match_phrase_prefix: {
							name: {
								query: searchQuery,
							},
						},
					},
				}
			);
			setResults(response.data.hits.hits);
		} catch (error) {
			console.error("Search Error:", error);
		}
	}, 100);

	return (
		<View style={styles.container}>
			<View style={styles.mapContainer}>
				<MapGuide mapPress={mapPress} landmarks={activeLandmarks} />
			</View>

			<KeyboardAvoidingView style={styles.overlay}>
				<View style={styles.searchContainer}>
					<TextInput
						style={styles.searchInput}
						placeholder="Search for destination"
						onChangeText={(text) => {
							setQuery(text);
							performSearch(text);
						}}
						value={query}
					/>
				</View>

				{!!results && (
					<View style={styles.resultsContainer}>
						<FlatList
							data={results}
							keyExtractor={(item) => item._id}
							renderItem={({ item }) => (
								<Item onPress={onLandmarkPress} item={item}></Item>
							)}
						/>
					</View>
				)}
			</KeyboardAvoidingView>
		</View>
	);
}

const styles = StyleSheet.create({
	container: {
		flex: 1,
	},
	itemSeparator: {
		height: 0.5,
		width: "100%",
		backgroundColor: "#C8C8C8",
	},
	searchContainer: {
		marginTop: 30, // Adjust if necessary
		backgroundColor: "white",
		borderRadius: 5,
		flex: 1,
		padding: 10,
		shadowColor: "#000",
		shadowOffset: { width: 0, height: 2 },
		shadowOpacity: 0.25,
		shadowRadius: 3.84,
		elevation: 5,
	},
	searchInput: {
		borderWidth: 1,
		borderColor: Colors.standartAppColor,
		padding: 10,
		borderRadius: 5,
		backgroundColor: "white",
	},
	overlay: {
		position: "absolute",
		top: 0,
		width: "100%",
		paddingHorizontal: 10,
	},
	mapContainer: {
		...StyleSheet.absoluteFillObject, // Makes the map fill the entire screen
	},
	itemStyle: {
		flex: 1,
		flexDirection: "row",
		padding: 10,
		height: 170,
	},
	resultsContainer: {
		zIndex: 0,
		width: "100%",
		backgroundColor: "rgba(255, 255, 255, 0.9)", // Semi-transparent background
		borderWidth: 1,
		borderColor: Colors.standartAppColor,
		borderRadius: 5,
		overflow: "hidden",
	},
	resultText: {
		padding: 10,
		fontSize: 16,
	},
});
