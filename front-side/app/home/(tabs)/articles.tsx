import { ArticleScoreComponent } from "@/components/ArticleScoreComponent";
import { Colors } from "@/constants/Colors";
import { ArticleScore } from "@/constants/enums";
import { BASE_URL } from "@/constants/request-api-constants";
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
  title: string;
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
      const url = BASE_URL + "/articles";
      const response = await axios.get<ArticleResponce>(url);
      setArticles(response.data.articles);
    } catch (error) {
      console.error(`Search error ${error}`);
    } finally {
      setLoaded(true);
    }
  };

  useEffect(() => {
    setArticles(articlesTest);
  }, []);

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
      <Text>{article.snippet}</Text>
      {/* TODO: for the near bright future */}
      {/* <View style={styles.userScore}>
				<ArticleScoreComponent score={article.score} setScore={setScore} />
			</View> */}
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
          keyboardShouldPersistTaps="always"
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
    marginTop: 10,
    shadowColor: "#000",
    alignSelf: "stretch",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 5,
    elevation: 2,
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
    paddingHorizontal: 10,
  },
  pressedListItem: {
    opacity: 0.2,
  },
  userScore: {
    marginTop: 15,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
  },
});

export default Articles;

const articlesTest = [
  {
    id: "test1",
    snippet:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum",
    content: "haha hahahahahh",
    title: "Article1",
    author: "Stas",
    score: ArticleScore.HUYNA_EBANAYA,
  },
  {
    id: "test2",
    snippet: "asaksjdasdjasl",
    content: "Article2",
    title: "Article2",
    author: "Stas",
    score: ArticleScore.LIKE,
  },
  {
    id: "test3",
    snippet: "asaksjdasdjasl",
    content: "Article3",
    title: "Article2",
    author: "Stas",
    score: ArticleScore.LIKE,
  },
  {
    id: "test4",
    snippet: "asaksjdasdjasl",
    content: "haha hahahahahh",
    title: "Article3",
    author: "Stas",
    score: ArticleScore.POHUY,
  },
  {
    id: "test5",
    snippet: "asaksjdasdjasl",
    content: "haha hahahahahh",
    title: "Article3",
    author: "Stas",
    score: ArticleScore.POHUY,
  },
];
