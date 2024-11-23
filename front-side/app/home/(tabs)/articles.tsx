import { Colors } from "@/constants/Colors";
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
} from "react-native";

const URL_STRING = "";

type ArticlesInfo = {
	id: string;
	title: string;
};

type ArticleResponce = {
	articles: ArticlesInfo[];
};

const articlesTest = [
	{
		id: "test1",
		content: "haha hahahahahh",
		title: "Ostis gavno",
	},
	{
		id: "test2",
		content: "haha hahahahahh",
		title: "Ostis dermo",
	},
	{
		id: "test3",
		content: "haha hahahahahh",
		title: "Ostis kal",
	},
];

const Articles = () => {
	const [loaded, setLoaded] = useState(false);
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
			style={[styles.item, { backgroundColor: "white" }]}
		>
			<Text style={[styles.title, { color: "black" }]}>{article.title}</Text>
		</TouchableOpacity>
	);

	return (
		<View
			style={{
				flex: 1,
				top: 20,
				alignItems: "center",
				justifyContent: "center",
			}}
		>
			<Text style={{ color: "white" }}>Articles!</Text>
			{loaded ? (
				<ActivityIndicator size="large" color={Colors.standartAppColor} />
			) : (
				<FlatList
					data={articles}
					keyExtractor={(item) => item.id}
					renderItem={({ item }) => <Item article={item} />}
				/>
			)}
		</View>
	);
};

const styles = StyleSheet.create({
	item: { padding: 20, marginVertical: 8 },
	title: { fontSize: 16 },
});

export default Articles;
