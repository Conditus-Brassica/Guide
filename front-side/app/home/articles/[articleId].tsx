import { UserInfo } from "@/app/login";
import { ArticleScore } from "@/constants/enums";
import { BASE_URL } from "@/constants/request-api-constants";
import { FirebaseAuth } from "@/FirebaseConfig";
import axios from "axios";
import { useLocalSearchParams } from "expo-router";
import React, { FC, useEffect, useState } from "react";
import { ScrollView, StyleSheet, View } from "react-native";
import Markdown from "react-native-markdown-display";
import { ArticlesInfo } from "../(tabs)/articles";
import { ArticleScoreComponent } from "@/components/ArticleScoreComponent";

type ArticleInfo = {
	content: string;
} & ArticlesInfo;

type ArticleReward = {
	articleId: string;
	timeOnPage: number;
	score: ArticleScore;
} & UserInfo;

const Article: FC = () => {
	const [isLoaded, setIsLoaded] = useState(false);
	const [articleDetails, setIsArticleDetails] = useState<ArticleInfo | null>(
		null
	);
	const [score, setScore] = useState<ArticleScore>(
		articleDetails?.score ?? ArticleScore.POHUY
	);
	const id = String(useLocalSearchParams());
	const user = String(FirebaseAuth.currentUser?.uid);

	const getArticle = async () => {
		try {
			const url = new URL(BASE_URL);
			url.searchParams.set("id", id);
			const response = await axios.get<ArticleInfo>(url.toString());
			setIsArticleDetails(response.data);
			setScore(response.data.score);
		} catch (error) {
			console.error(`HTTP error: ${error}`);
		} finally {
			setIsLoaded(true);
		}
	};

	const postArticleReward = async (articleReward: ArticleReward) => {
		try {
			const url = new URL(BASE_URL);
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
			postArticleReward({
				articleId: id,
				timeOnPage: duration,
				score: score,
				userId: user,
			});
		};
	}, []);

	return (
		<ScrollView
			contentInsetAdjustmentBehavior="automatic"
			style={{ height: "100%" }}
		>
			<Markdown>{articleDetails?.content}</Markdown>
			<ArticleScoreComponent
				score={articleDetails?.score ?? ArticleScore.POHUY}
				setScore={setScore}
			/>
		</ScrollView>
	);
};

export default Article;
