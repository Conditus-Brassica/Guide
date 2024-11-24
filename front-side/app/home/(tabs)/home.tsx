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
		<View style={{ flex: 1 }}>
			<Text style={styles.textStyle}>{item.name}</Text>
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
			<View style={styles.searchContainer}>
				<SearchBase
					index="landmarks_index"
					credentials="elastic:mypassword"
					url="http://192.168.1.123:9200"
					appbaseConfig={{
						recordAnalytics: true,
						enableQueryRules: true,
						userId: user?.email,
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
						renderNoSuggestion={() => (
							<Text>Нет подходящих достопримечательностей</Text>
						)}
						enableRecentSearches
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
			</View>
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
		flex: 0.13,
		top: 25,
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
