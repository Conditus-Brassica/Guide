import { Icon } from "@rneui/base";
import { View } from "react-native";
import { ArticleScore } from "@/constants/enums";
import { StyleSheet } from "react-native";
import { ArticlesInfo } from "../app/home/(tabs)/articles";
import { FC } from "react";

type PropsType = Pick<ArticlesInfo, "score"> & {
	setScore: (score: ArticleScore) => void;
};

export const ArticleScoreComponent: FC<PropsType> = ({
	score,
	setScore,
}: PropsType) => {
	return (
		<View style={styles.userScore}>
			{score === ArticleScore.LIKE ? (
				<Icon
					name="heart"
					size={40}
					type="ionicon"
					color="red"
					onPress={() => setScore(ArticleScore.POHUY)}
				/>
			) : (
				<Icon
					name="heart-outline"
					size={40}
					type="ionicon"
					color="black"
					onPress={() => setScore(ArticleScore.LIKE)}
				/>
			)}
			{score === ArticleScore.HUYNA_EBANAYA ? (
				<Icon
					name="heart-dislike"
					size={40}
					type="ionicon"
					color="red"
					onPress={() => setScore(ArticleScore.POHUY)}
				/>
			) : (
				<Icon
					name="heart-dislike-outline"
					size={40}
					type="ionicon"
					color="black"
					onPress={() => setScore(ArticleScore.HUYNA_EBANAYA)}
				/>
			)}
		</View>
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
