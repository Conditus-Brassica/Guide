//@ts-nocheck
import React from "react";
import { FirebaseAuth } from "@/FirebaseConfig";
import {
	ActivityIndicator,
	SafeAreaView,
	StyleSheet,
	View,
	Text,
	FlatList,
	Image,
} from "react-native";
import { MapGuide } from "@/components/MapComponent/MapGuide";

import {
	SearchBase,
	SearchBox,
	SearchComponent,
} from "@appbaseio/react-native-searchbox";
import {
	AntDesign,
	Feather,
	Ionicons,
	MaterialIcons,
} from "@expo/vector-icons";

const renderResultItem = ({ item }) => (
	<View style={styles.itemStyle}>
		<Image
			style={styles.image}
			source={{
				uri: item.image,
			}}
			resizeMode="contain"
		/>
		<View style={{ flex: 1 }}>
			<Text style={styles.textStyle}>{item.original_title}</Text>
			<Text style={styles.textStyle}>by {item.authors}</Text>
			<View style={styles.star}>
				{Array(item.average_rating_rounded)
					.fill("x")
					.map((i, index) => (
						<AntDesign
							key={item._id + `_${index}`}
							name="star"
							size={24}
							color="gold"
						/>
					))}
				<Text style={styles.rating}>({item.average_rating} avg)</Text>
			</View>
			<Text>Pub {item.original_publication_year}</Text>
		</View>
	</View>
);

const renderItemSeparator = () => {
	return <View style={styles.itemSeparator} />;
};

export default function App() {
	const user = FirebaseAuth.currentUser;

	return (
		<View style={styles.container}>
			<SafeAreaView style={styles.searchContainer}>
				<SearchBase
					index="landmarks_index"
					url="http://localhost:9200"
					appbaseConfig={{
						recordAnalytics: true,
						enableQueryRules: true,
						userId: user?.email,
						customEvents: {
							platform: "ios",
							device: "iphoneX",
						},
					}}
				>
					<SearchBox
						id="search-component"
						dataField={[
							{
								field: "name",
								weight: 2,
							},
							{
								field: "name.suggest",
								weight: 3,
							},
						]}
						renderNoSuggestion={() => <Text>No suggestions found</Text>}
						enableRecentSearches
						goBackIcon={(props) => <Ionicons {...props} />}
						autoFillIcon={(props) => (
							<Feather name="arrow-up-left" {...props} />
						)}
						recentSearchIcon={(props) => (
							<MaterialIcons name="history" {...props} />
						)}
						searchBarProps={{
							searchIcon: (props) => <MaterialIcons name="search" {...props} />,
							clearIcon: (props) => <MaterialIcons name="clear" {...props} />,
						}}
					/>
					<SearchComponent
						id="result-component"
						dataField="name"
						size={10}
						react={{
							and: ["search-component", "author-filter"],
						}}
						preserveResults
					>
						{({ results, loading, size, from, setValue, setFrom }) => {
							return (
								<View>
									{loading && !results.data.length ? (
										<ActivityIndicator
											style={styles.loader}
											size="large"
											color="#000"
										/>
									) : (
										<View>
											{!results.data.length ? (
												<Text style={styles.resultStats}>No results found</Text>
											) : (
												<View style={styles.resultContainer}>
													<Text style={styles.resultStats}>
														{results.numberOfResults} results found in{" "}
														{results.time}ms
													</Text>
													<FlatList
														data={results.data}
														keyboardShouldPersistTaps={"handled"}
														keyExtractor={(item) => item._id}
														ItemSeparatorComponent={renderItemSeparator}
														renderItem={renderResultItem}
														onEndReached={() => {
															const offset = (from || 0) + size;
															if (results.numberOfResults > offset) {
																setFrom((from || 0) + size);
															}
														}}
														onEndReachedThreshold={0.5}
														ListFooterComponent={
															loading ? (
																<ActivityIndicator size="large" color="#000" />
															) : null
														}
													/>
												</View>
											)}
										</View>
									)}
								</View>
							);
						}}
					</SearchComponent>
				</SearchBase>
			</SafeAreaView>
			<View style={styles.mapContainer}>
				<MapGuide />
			</View>
		</View>
	);
}

const styles = StyleSheet.create({
	container: {
		flex: 1,
	},
	loader: {
		marginTop: 50,
	},
	itemSeparator: {
		height: 0.5,
		width: "100%",
		backgroundColor: "#C8C8C8",
	},
	searchContainer: {
		flex: 0.1,
	},
	mapContainer: { flex: 0.9 },
	image: {
		width: 100,
		marginRight: 10,
	},
	itemStyle: {
		flex: 1,
		flexDirection: "row",
		padding: 10,
		height: 170,
	},
	star: {
		flexDirection: "row",
		paddingBottom: 5,
	},
	textStyle: {
		flexWrap: "wrap",
		paddingBottom: 5,
	},
	resultStats: {
		padding: 10,
	},
	rating: {
		marginLeft: 10,
	},
});
