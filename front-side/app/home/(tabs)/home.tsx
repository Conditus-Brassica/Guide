import React, { useEffect, useState } from "react";
import { FirebaseAuth } from "@/FirebaseConfig";
import {
	FlatList,
	StyleSheet,
	TextInput,
	View,
	Text,
	TouchableOpacity,
} from "react-native";
import { MapGuide } from "@/components/MapComponent/MapGuide";
import axios from "axios";
import { ELASTIC_URL } from "@/constants/request-api-constants";
import { Colors } from "@/constants/Colors";
import { LatLng } from "react-native-maps";
import { setStatusBarHidden } from "expo-status-bar";
import * as Location from "expo-location";

type landmarkInfo = {
	_id: string;
	_source: LandmarkSearchDetails;
};

type LandmarkSearchDetails = {
	name: string;
	coordinates: LatLng;
};

const Item = ({ item }: { item: landmarkInfo }) => (
	<TouchableOpacity style={styles.resultText}>
		<Text>{item._source.name}</Text>
	</TouchableOpacity>
);

export default function App() {
	const user = FirebaseAuth.currentUser;
	setStatusBarHidden(false);

	const [results, setResults] = useState<landmarkInfo[]>([]);
	const [query, setQuery] = useState("");

	const [location, setLocation] = useState<Location.LocationObject | null>(
		null
	);
	const [errorMsg, setErrorMsg] = useState<string | null>(null);

	let text = "Waiting...";
	if (errorMsg) {
		text = errorMsg;
	} else if (location) {
		text = JSON.stringify(location);
	}

	const performSearch = async (searchQuery: string) => {
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
	};

	useEffect(() => {
		async function getCurrentLocation() {
			let { status } = await Location.requestForegroundPermissionsAsync();
			if (status !== "granted") {
				setErrorMsg("Permission to access location was denied");
				return;
			}

			let location = await Location.getCurrentPositionAsync({});
			setLocation(location);
		}

		getCurrentLocation();
	}, []);

	console.log(location);
	return (
		<View style={styles.container}>
			<View style={styles.mapContainer}>
				<MapGuide />
			</View>

			<View style={styles.overlay}>
				<View style={styles.searchContainer}>
					<TextInput
						style={styles.searchInput}
						placeholder="Seatch for destination"
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
							renderItem={({ item }) => <Item item={item}></Item>}
						/>
					</View>
				)}
			</View>
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
