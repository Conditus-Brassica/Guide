import { Colors } from "@/constants/Colors";
import { ArticleScore } from "@/constants/enums";
import axios from "axios";
import { router } from "expo-router";
import { useEffect, useState } from "react";
import {
	ActivityIndicator,
	FlatList,
	ScrollView,
	StyleSheet,
	Text,
	TouchableOpacity,
	View,
	TextInput,
} from "react-native";

const URL_STRING = "";

export type ArticlesInfo = {
	id: string;
	title: string;
	author: string;
	score: ArticleScore;
};

type ArticleResponce = {
	articles: ArticlesInfo[];
};

const articlesTest = [
	{
		id: "test1",
		content: "haha hahahahahh",
		title: "Article1",
		author: "Stas",
		score: ArticleScore.POHUY,
	},
	{
		id: "test2",
		content: "Article2",
		title: "Article2",
		author: "Stas",
		score: ArticleScore.POHUY,
	},
	{
		id: "test3",
		content: "Article3",
		title: "Article2",
		author: "Stas",
		score: ArticleScore.POHUY,
	},
	{
		id: "test4",
		content: "haha hahahahahh",
		title: "Article3",
		author: "Stas",
		score: ArticleScore.POHUY,
	},
	{
		id: "test5",
		content: "haha hahahahahh",
		title: "Article3",
		author: "Stas",
		score: ArticleScore.POHUY,
	},
];

const Articles = () => {
	const [loaded, setLoaded] = useState(true);
	const [articles, setArticles] = useState<ArticlesInfo[]>(articlesTest);

	const getArticles = async () => {
		try {
			const url = new URL(URL_STRING);
			const response = await axios.get<ArticleResponce>(url.toString());
			setArticles(response.data.articles);
		} catch (error) {
			console.error(`Search error ${error}`);
		} finally {
			setLoaded(true);
		}
	};

	//TODO: Remove commenting when API will be ready
	// useEffect(() => {
	// 	getArticles();
	// }, []);

	const Item = ({ article }: { article: ArticlesInfo }) => (
		<TouchableOpacity
			onPress={() => {
				router.navigate(`/home/articles/${article.id}`);
			}}
			style={styles.item}
		>
			<Text style={styles.title}>{article.title}</Text>
		</TouchableOpacity>
	);

	return (
		<View style={styles.scrollView}>
			<View style={styles.searchContainer}>
				<TextInput
					style={styles.searchInput}
					placeholder="Search for articles"
					onChangeText={(text) => {}}
				/>
			</View>
			{loaded ? (
				<FlatList
					style={styles.flatList}
					data={articles}
					keyExtractor={(item) => item.id}
					renderItem={({ item }) => <Item article={item} />}
				/>
			) : (
				<ActivityIndicator size="large" color={Colors.standartAppColor} />
			)}
		</View>
	);
};

const styles = StyleSheet.create({
	item: {
		padding: 15,
		marginVertical: 10,
		marginHorizontal: 20,
		backgroundColor: "white",
		borderRadius: 10,
		shadowColor: "#000",
		shadowOffset: { width: 0, height: 2 },
		shadowOpacity: 0.1,
		shadowRadius: 5,
		elevation: 2,
	},
	title: {
		fontSize: 18,
		color: "#333",
		fontWeight: "500",
	},
	scrollView: {
		top: 20,
		flex: 1,
	},
	searchContainer: {
		backgroundColor: "white",
		borderRadius: 10,
		padding: 10,
		margin: 10,
		flex: 0,
		borderColor: Colors.standartAppColor,
		borderWidth: 2,
		shadowColor: "#000",
		shadowOffset: { width: 0, height: 2 },
		shadowOpacity: 0.1,
		shadowRadius: 3,
		elevation: 3,
	},
	searchInput: {
		borderWidth: 1,
		borderColor: Colors.standartAppColor,
		padding: 10,
		borderRadius: 8,
		backgroundColor: "white",
		color: "#333",
	},
	flatList: {
		flex: 3,
		paddingHorizontal: 10,
	},
});

export default Articles;
