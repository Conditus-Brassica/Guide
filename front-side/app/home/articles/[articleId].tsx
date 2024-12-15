import { UserInfo } from "@/app/login";
import { ArticleScore } from "@/constants/enums";
import { BASE_URL } from "@/constants/request-api-constants";
import { FirebaseAuth } from "@/FirebaseConfig";
import axios from "axios";
import { useLocalSearchParams } from "expo-router";
import React, { FC, useEffect, useRef, useState } from "react";
import { ScrollView, StyleSheet, View } from "react-native";
import Markdown from "react-native-markdown-display";
import { ArticlesInfo } from "../(tabs)/articles";
import { ArticleScoreComponent } from "@/components/ArticleScoreComponent";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { articleRewardKey } from "@/constants/async-storage-constants";

type ArticleInfo = {
  content: string;
} & ArticlesInfo;

type ArticleReward = {
  articleName: string;
  timeOnPage: number;
  score: ArticleScore;
} & UserInfo;

const GetArticleInfoFromStorage = async (id: string) => {
  const articlesStore = await AsyncStorage.getItem("Articles_State");
  const articles = JSON.parse(articlesStore ?? "") as Array<ArticleReward>;
  if (articles.some((article) => article.articleName == id)) {
    const article = articles.find((article) => article.articleName == id);
    return article as ArticleReward;
  }
  return undefined;
};

const Article: FC = () => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [articleDetails, setIsArticleDetails] = useState<ArticleInfo | null>(
    null
  );
  const initialTime = useRef(0);
  const [score, setScore] = useState<ArticleScore>(
    articleDetails?.score ?? ArticleScore.POHUY
  );
  const id = String(useLocalSearchParams());
  const user = String(FirebaseAuth.currentUser?.uid);

  const firstInteraction = async (articleDetails: ArticleInfo) => {
    await axios.post(BASE_URL + "/articles/state/interation_started", [
      { title: articleDetails.title },
    ]);
  };

  const getArticle = async () => {
    try {
      const url = BASE_URL + "/articles/" + id;
      const response = await axios.get<ArticleInfo>(url);
      setIsArticleDetails(response.data);
      const articleInfo = await GetArticleInfoFromStorage(id);
      if (articleInfo) {
        setScore(articleInfo.score);
        firstInteraction(response.data);
        initialTime.current = articleInfo.timeOnPage;
      } else {
        setScore(response.data.score);
      }
    } catch (error) {
      console.error(`HTTP error: ${error}`);
    } finally {
      setIsLoaded(true);
    }
  };

  const postArticleReward = async (articleReward: ArticleReward) => {
    try {
      var articlesReward = JSON.stringify(articleReward);
      await AsyncStorage.mergeItem(articleRewardKey, articlesReward);
    } catch (error) {
      console.error(`HTTP error: ${error}`);
    }
  };

  useEffect(() => {
    getArticle();
    const entryTime = Date.now();
    return () => {
      if (!articleDetails) return;
      const exit = Date.now();
      const duration = exit - entryTime + initialTime.current;
      postArticleReward({
        articleName: articleDetails.title,
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
