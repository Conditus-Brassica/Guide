import React, { useEffect, useState } from "react";
import {
	FlatList,
	StyleSheet,
	TextInput,
	View,
	Text,
	TouchableOpacity,
	Keyboard,
	KeyboardAvoidingView,
	Alert,
	ActivityIndicator,
} from "react-native";
import * as Location from "expo-location";
import { MapGuide } from "@/components/MapComponent/MapGuide";
import axios from "axios";
import { ELASTIC_URL } from "@/constants/request-api-constants";
import { Colors } from "@/constants/Colors";
import { setStatusBarHidden } from "expo-status-bar";
import { landmarkInfo } from "@/types/landmarks-types";
import { useDebouncedCallback } from "use-debounce";
import { useMapStore } from "@/hooks/useMapStore";

const Item = ({
	item,
	field,
	onPress,
}: {
	item: landmarkInfo;
	field: string;
	onPress: (item: landmarkInfo, field: string) => void;
}) => (
	<TouchableOpacity
		style={styles.resultText}
		onPress={() => {
			onPress(item, field);
		}}
	>
		<Text>{item._source.name}</Text>
	</TouchableOpacity>
);

export default function App() {
	setStatusBarHidden(false);
	const [location, setLocation] = useState<Location.LocationObject | null>(
		null
	);
	const [results, setResults] = useState<landmarkInfo[]>([]);
	const [activeLandmarks, setActiveLandmarks] = useState<landmarkInfo[]>([]);
	const [originValue, setOriginValue] = useState("");
	const [destinationValue, setDestinationValue] = useState("");
	const activeRoute = useMapStore((state) => state.activeRoute);
	const setRouteOrigin = useMapStore((state) => state.setRouteOrigin);
	const setRouteDestination = useMapStore((state) => state.setRouteDestination);
	const setInitialPosition = useMapStore((state) => state.setInitialCoords);
	const [loading, setLoading] = useState(false);

	const mapPress = () => {
		setResults([]);
		Keyboard.dismiss();
	};

	const onLandmarkPress = (item: landmarkInfo, field: string) => {
		if (field === "origin") {
			setRouteOrigin(item._source.coordinates);
			setOriginValue("");
		} else {
			setRouteDestination(item._source.coordinates);
			setRouteOrigin(location?.coords);
			setDestinationValue("");
		}
		setActiveLandmarks([...activeLandmarks, item]);
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
	}, 200);

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
		<View style={styles.container}>
			<View style={styles.mapContainer}>
				<MapGuide mapPress={mapPress} landmarks={activeLandmarks} />
			</View>

			<KeyboardAvoidingView style={styles.overlay}>
				<View style={styles.searchContainer}>
					{!!activeRoute && activeRoute.destination != null && (
						<TextInput
							style={styles.searchInput}
							placeholder="Start point"
							onChangeText={(text) => {
								setOriginValue(text);
								performSearch(text);
							}}
							value={originValue}
						/>
					)}
					<TextInput
						style={styles.searchInput}
						placeholder="Search for destination"
						onChangeText={(text) => {
							setDestinationValue(text);
							performSearch(text);
						}}
						value={destinationValue}
					/>
				</View>

				{results.length > 0 && (
					<View style={styles.resultsContainer}>
						<FlatList
							data={results}
							keyExtractor={(item) => item._id}
							keyboardShouldPersistTaps="always"
							renderItem={({ item }) => (
								<Item
									onPress={onLandmarkPress}
									item={item}
									field={activeRoute?.destination ? "origin" : "destination"}
								></Item>
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
		borderWidth: 2,
		borderColor: Colors.standartAppColor,
		borderRadius: 10,
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
		...StyleSheet.absoluteFillObject,
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
	loaderContainer: {
		flex: 1,
		justifyContent: "center",
		alignItems: "center",
	},
});
