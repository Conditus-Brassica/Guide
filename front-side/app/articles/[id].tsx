import { Navigator, useNavigation } from "expo-router";
import { FC, useLayoutEffect } from "react";
import { Text, View } from "react-native";

type PropsType = {
	title: string;
	content: string;
};

const Article: FC<PropsType> = (article) => {
	const navigation = useNavigation();
	useLayoutEffect(() => {
		navigation.setOptions({
			headerTitle: article.title,
		});
	});
	return (
		<View>
			<Text style={{ top: 20 }} children={article.content} />
		</View>
	);
};

export default Article;
