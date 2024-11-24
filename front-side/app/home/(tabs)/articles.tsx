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
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

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
		title: "Ostis gavno",
		author: "Stas",
		score: ArticleScore.POHUY,
	},
	{
		id: "test2",
		content: "haha hahahahahh",
		title: "Ostis dermo",
		author: "Stas",
		score: ArticleScore.POHUY,
	},
	{
		id: "test3",
		content: "haha hahahahahh",
		title: "Ostis kal",
		author: "Stas",
		score: ArticleScore.POHUY,
	},
	{
		id: "test4",
		content: "haha hahahahahh",
		title: "Ostis kal",
		author: "Stas",
		score: ArticleScore.POHUY,
	},
	{
		id: "test5",
		content: "haha hahahahahh",
		title: "Ostis kal",
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
		padding: 20,
		marginVertical: 8,
		backgroundColor: "white",
		borderColor: Colors.standartAppColor,
		borderWidth: 2,
	},
	title: { fontSize: 24, color: "black", fontWeight: "600" },
	scrollView: {
		top: 20,
	},
	flatList: {},
});

export default Articles;
