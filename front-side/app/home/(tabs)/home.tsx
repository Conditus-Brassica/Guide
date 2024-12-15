import React, { useEffect, useRef, useState } from "react";
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
	Modal,
} from "react-native";
import StarRating from "react-native-star-rating-widget";
import * as Location from "expo-location";
import { MapGuide } from "@/components/MapComponent/MapGuide";
import axios from "axios";
import { BASE_URL, ELASTIC_URL } from "@/constants/request-api-constants";
import { Colors } from "@/constants/Colors";
import { setStatusBarHidden } from "expo-status-bar";
import {
	landmarkInfo,
	Recommendation,
	RecommendationInfo,
} from "@/types/landmarks-types";
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

	const [originSearch, setOriginSearch] = useState(false);
	const [rating, setRating] = useState(2.5);
	const primaryRecommendation = useRef<Recommendation[]>([]);
	const [recommendation, setRecommendation] = useState<Recommendation[]>([]);
	const [results, setResults] = useState<landmarkInfo[]>([]);
	const [activeLandmarks, setActiveLandmarks] = useState<landmarkInfo[]>([]);
	const [originValue, setOriginValue] = useState("");
	const [destinationValue, setDestinationValue] = useState("");

	const activeRoute = useMapStore((state) => state.activeRoute);
	const setRouteOrigin = useMapStore((state) => state.setRouteOrigin);
	const setRouteDestination = useMapStore((state) => state.setRouteDestination);
	const setInitialPosition = useMapStore((state) => state.setInitialCoords);
	const [loading, setLoading] = useState(true);
	const [modalVisible, setModalVisible] = useState(false);

	const resetAll = () => {
		// Reset component states
		setOriginSearch(false);
		setRating(2.5);
		primaryRecommendation.current = [];
		setRecommendation([]);
		setResults([]);
		setActiveLandmarks([]);
		setOriginValue("");
		setDestinationValue("");

		// Reset global store states
		setInitialPosition(location!.coords);
		setRouteOrigin(undefined);
		setRouteDestination(undefined);
	};

	const mapPress = () => {
		setResults([]);
		Keyboard.dismiss();
	};

	const onLandmarkPress = (item: landmarkInfo, field: string) => {
		if (field === "origin") {
			setRouteOrigin(item._source.coordinates);
			setOriginValue(item._source.name);
		} else {
			setRouteDestination(item._source.coordinates);
			setRouteOrigin({
				latitude: location!.coords.latitude,
				longitude: location!.coords.longitude,
			});
			setDestinationValue(item._source.name);
		}
		if (!activeLandmarks.some((landmark) => landmark._id === item._id)) {
			if (activeLandmarks.length === 0) {
				setActiveLandmarks([item]);
			} else {
				setActiveLandmarks([activeLandmarks[activeLandmarks.length - 1], item]);
			}
		}
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

	const getRecommendations = async () => {
		try {
			const response = await axios.post<RecommendationInfo>(
				`${BASE_URL}/route/find_recommendations_by_coordinates`,
				{
					coordinates_of_points: [
						{
							latitude: activeRoute?.origin!.latitude,
							longitude: activeRoute?.origin!.longitude,
						},
						{
							latitude: activeRoute?.destination!.latitude,
							longitude: activeRoute?.destination!.longitude,
						},
					],
					maximum_amount_of_recommendations: 5,
				}
			);
			setRecommendation(response.data.recommendation);
			primaryRecommendation.current = response.data.recommendation;
		} catch (error) {
			console.error("Search Error:", error);
		}
	};

	const sendRating = async () => {
		try {
			await axios.post(`${BASE_URL}/route/post_result_of_recommendations`, {
				user_reward: rating,
				primary_Recommendation: primaryRecommendation.current,
				result_recommendations: recommendation,
			});
			setModalVisible(false);
		} catch (error) {
			console.error("Search Error:", error);
		}
	};

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
		return (
			<View style={styles.loaderContainer}>
				<ActivityIndicator size="large" color={Colors.standartAppColor} />
			</View>
		);
	}

	return (
		<View style={styles.container}>
			<View style={styles.mapContainer}>
				<MapGuide
					mapPress={mapPress}
					landmarks={activeLandmarks.map((landmark) => landmark._source)}
					recommendations={recommendation}
					setRecommendations={setRecommendation}
				/>
			</View>

			<KeyboardAvoidingView style={styles.overlay}>
				<View style={styles.searchContainer}>
					{!!activeRoute && activeRoute.destination != null && (
						<TextInput
							style={styles.searchInput}
							placeholder="Start point"
							onChangeText={(text) => {
								setOriginSearch(true);
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
							setOriginSearch(false);
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
									field={originSearch ? "origin" : "destination"}
								></Item>
							)}
						/>
					</View>
				)}
			</KeyboardAvoidingView>
			{activeRoute?.origin &&
				activeRoute?.destination &&
				recommendation.length === 0 && (
					<TouchableOpacity
						style={styles.recommendationButton}
						onPress={() => {
							//Dont forget to remove modal visibility
							setModalVisible(true);
							// getRecommendations();
						}}
					>
						<Text style={styles.recommendationButtonText}>
							Get recommendations
						</Text>
					</TouchableOpacity>
				)}
			{recommendation.length > 0 && (
				<TouchableOpacity
					style={styles.recommendationButton}
					onPress={() => {
						setModalVisible(true);
					}}
				>
					<Text style={styles.recommendationButtonText}>End the Journey</Text>
				</TouchableOpacity>
			)}
			<Modal
				animationType="slide"
				transparent={true}
				visible={modalVisible}
				onRequestClose={() => setModalVisible(false)}
			>
				<View style={styles.modalContainer}>
					<View style={styles.modalContent}>
						<Text style={styles.modalTitle}>Rate Your Journey</Text>
						<StarRating
							rating={rating}
							maxStars={5}
							onChange={setRating}
							starSize={40}
							color={Colors.standartAppColor}
						/>
						<Text style={styles.ratingText}>Your rating: {rating} stars</Text>
						<TouchableOpacity
							style={styles.closeButton}
							onPress={() => {
								setModalVisible(false);
								sendRating();
								resetAll();
							}}
						>
							<Text style={styles.closeButtonText}>Close</Text>
						</TouchableOpacity>
					</View>
				</View>
			</Modal>
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
	recommendationButton: {
		position: "absolute",
		bottom: 10, // Adjust this value to control the distance from the bottom
		alignSelf: "center",
		backgroundColor: Colors.standartAppColor,
		paddingVertical: 15,
		paddingHorizontal: 20,
		borderRadius: 30,
		shadowColor: "#000",
		shadowOffset: { width: 0, height: 2 },
		shadowOpacity: 0.25,
		shadowRadius: 3.84,
		elevation: 5,
	},
	recommendationButtonText: {
		color: "white",
		fontSize: 16,
		fontWeight: "bold",
		textAlign: "center",
	},
	modalContainer: {
		flex: 1,
		justifyContent: "center",
		alignItems: "center",
		backgroundColor: "rgba(0, 0, 0, 0)",
	},
	modalContent: {
		width: "80%",
		backgroundColor: "white",
		padding: 20,
		borderRadius: 10,
		alignItems: "center",
	},
	modalTitle: {
		fontSize: 18,
		fontWeight: "bold",
		marginBottom: 10,
	},
	ratingText: {
		marginTop: 10,
		fontSize: 16,
	},
	closeButton: {
		marginTop: 20,
		padding: 10,
		backgroundColor: Colors.standartAppColor,
		borderRadius: 5,
	},
	closeButtonText: {
		color: "white",
		fontWeight: "bold",
	},
});
