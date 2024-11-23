import { ArticleScore } from "@/constants/enums";
import axios from "axios";
import { useLocalSearchParams } from "expo-router";
import { FC, useEffect, useState } from "react";
import { ScrollView, Text, View } from "react-native";
import Markdown from "react-native-markdown-display";

const URL_STRING = "";

type ArticleInfo = {
	id: string;
	title: string;
	author: string;
	content: string;
	score: ArticleScore;
};

type ArticleReward = {
	timeOnPage: number;
	score: ArticleScore;
};

const Article: FC = () => {
	const [isLoaded, setIsLoaded] = useState(false);
	const [atricleDetails, setIsArticleDetails] = useState<ArticleInfo | null>(
		null
	);
	const [entryTime, setEntryTime] = useState<number | null>(null);
	const [score, setScore] = useState<ArticleScore>(ArticleScore.POHUY);
	const { id } = useLocalSearchParams();

	const getArticle = async () => {
		try {
			const url = new URL(URL_STRING);
			url.searchParams.set("id", String(id));
			const response = await axios.get<ArticleInfo>(url.toString());
			setIsArticleDetails(response.data);
		} catch (error) {
			console.error(`HTTP error: ${error}`);
		} finally {
			setIsLoaded(true);
		}
	};

	const postArticleReward = async (articleReward: ArticleReward) => {
		try {
			const url = new URL(URL_STRING);
			url.searchParams.set("id", String(id));
			navigator.sendBeacon(url.toString(), JSON.stringify(articleReward));
		} catch (error) {
			console.error(`HTTP error: ${error}`);
		}
	};

	useEffect(() => {
		getArticle();
		const entryTime = Date.now();
		return () => {
			const exit = Date.now();
			const duration = exit - entryTime;
			postArticleReward({ timeOnPage: duration, score: score });
		};
	}, []);

	return (
		<ScrollView
			contentInsetAdjustmentBehavior="automatic"
			style={{ height: "100%" }}
		>
			<Markdown>{atricleDetails?.content}</Markdown>
		</ScrollView>
	);
};

export default Article;
