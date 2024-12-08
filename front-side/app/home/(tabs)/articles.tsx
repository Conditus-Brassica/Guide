import { ArticleScoreComponent } from "@/components/ArticleScoreComponent";
import { Colors } from "@/constants/Colors";
import { ArticleScore } from "@/constants/enums";
import { BASE_URL } from "@/constants/request-api-constants";
import { ListItem } from "@rneui/base";
import axios from "axios";
import { router } from "expo-router";
import { useEffect, useState } from "react";
import {
	ActivityIndicator,
	FlatList,
	StyleSheet,
	Text,
	TouchableOpacity,
	View,
	TextInput,
} from "react-native";

export type ArticlesInfo = {
	id: string;
	ListItem: string;
	author: string;
	snippet: string;
	score: ArticleScore;
};

type ArticleResponce = {
	articles: ArticlesInfo[];
};

const Articles = () => {
	const [loaded, setLoaded] = useState(true);
	const [articles, setArticles] = useState<ArticlesInfo[]>(articlesTest);
	const [score, setScore] = useState<ArticleScore>(ArticleScore.POHUY);

	const getArticles = async () => {
		try {
			const url = new URL(BASE_URL);
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
			<ListItem containerStyle={styles.ListItem}>
				<ListItem.Content>
					<ListItem.Title style={styles.title}>
						{article.ListItem}
					</ListItem.Title>
					<Text>{article.snippet}</Text>
				</ListItem.Content>
				<ArticleScoreComponent score={article.score} setScore={setScore} />
			</ListItem>
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
		backgroundColor: "white",
		borderColor: Colors.standartAppColor,
		borderWidth: 2,
		shadowColor: "#000",
		alignSelf: "stretch",
		shadowOffset: { width: 0, height: 2 },
		shadowOpacity: 0.1,
		shadowRadius: 5,
		elevation: 2,
	},
	ListItem: {
		backgroundColor: "white",
	},
	title: {
		color: "black",
		fontWeight: "bold",
		fontSize: 24,
	},
	scrollView: {
		top: 20,
		flex: 1,
		backgroundColor: Colors.standartAppGrey,
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
		alignSelf: "stretch",
		backgroundColor: "white",
		color: "#333",
	},
	flatList: {
		flex: 3,
	},
	userScore: {
		flexDirection: "row",
		columnGap: 10,
		alignItems: "center",
		justifyContent: "center",
	},
});

export default Articles;

const articlesTest = [
	{
		id: "test1",
		snippet: "asaksjdasdjasl",
		content: "haha hahahahahh",
		ListItem: "Article1",
		author: "Stas",
		score: ArticleScore.POHUY,
	},
	{
		id: "test2",
		snippet: "asaksjdasdjasl",
		content: "Article2",
		ListItem: "Article2",
		author: "Stas",
		score: ArticleScore.POHUY,
	},
	{
		id: "test3",
		snippet: "asaksjdasdjasl",
		content: "Article3",
		ListItem: "Article2",
		author: "Stas",
		score: ArticleScore.POHUY,
	},
	{
		id: "test4",
		snippet: "asaksjdasdjasl",
		content: "haha hahahahahh",
		ListItem: "Article3",
		author: "Stas",
		score: ArticleScore.POHUY,
	},
	{
		id: "test5",
		snippet: "asaksjdasdjasl",
		content: "haha hahahahahh",
		ListItem: "Article3",
		author: "Stas",
		score: ArticleScore.POHUY,
	},
];
