import { UserInfo } from "@/app/login";
import { ArticleScore } from "@/constants/enums";
import { BASE_URL } from "@/constants/request-api-constants";
import { FirebaseAuth } from "@/FirebaseConfig";
import axios from "axios";
import { useLocalSearchParams } from "expo-router";
import React, { FC, useEffect, useState } from "react";
import { Image, ScrollView, StyleSheet, View } from "react-native";
import Markdown from "react-native-markdown-display";
import { ArticlesInfo } from "../(tabs)/articles";
import Icon from "react-native-ionicons";

type ArticleInfo = {
	content: string;
} & ArticlesInfo;

type ArticleReward = {
	timeOnPage: number;
	score: ArticleScore;
} & UserInfo;

const Article: FC = () => {
	const [isLoaded, setIsLoaded] = useState(false);
	const [atricleDetails, setIsArticleDetails] = useState<ArticleInfo | null>(
		null
	);
	const [entryTime, setEntryTime] = useState<number | null>(null); //TODO: Check if i need this
	const [score, setScore] = useState<ArticleScore>(ArticleScore.POHUY); //TODO: Possibly this state is also not needed
	const { id } = useLocalSearchParams();
	const user = String(FirebaseAuth.currentUser?.email);

	const getArticle = async () => {
		try {
			const url = new URL(BASE_URL);
			url.searchParams.set("id", String(id));
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
			postArticleReward({ timeOnPage: duration, score: score, email: user });
		};
	}, []);

	return (
		<ScrollView
			contentInsetAdjustmentBehavior="automatic"
			style={{ height: "100%" }}
		>
			<Markdown>{atricleDetails?.content}</Markdown>
			<View style={styles.userScore}>
				{atricleDetails?.score === ArticleScore.LIKE ? (
					<Icon name="heart" />
				) : (
					<Icon name="heart-outline" />
				)}
				{atricleDetails?.score === ArticleScore.HUYNA_EBANAYA ? (
					<Icon name="heart-dislike" />
				) : (
					<Icon name="heart-dislike-outline" />
				)}
			</View>
		</ScrollView>
	);
};

const styles = StyleSheet.create({
	userScore: {
		flexDirection: "row",
		columnGap: 10,
		alignItems: "center",
		justifyContent: "center",
	},
});

export default Article;
