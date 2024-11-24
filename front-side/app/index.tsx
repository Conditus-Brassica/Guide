import { Colors } from "@/constants/Colors";
import { Image } from "expo-image";
import { router } from "expo-router";
import React, { useEffect, useState } from "react";
import {
	StyleSheet,
	View,
	Text,
	TouchableOpacity,
	ActivityIndicator,
} from "react-native";

const Index = () => {
	const [imageLoaded, setImageLoaded] = useState(false);

	return (
		<View style={styles.beginContainer}>
			<View style={styles.logoContainer}>
				{!imageLoaded && (
					<ActivityIndicator size="large" color={Colors.standartAppColor} />
				)}

				<Image
					style={styles.logo}
					contentFit="contain"
					source={require("./../assets/images/app-icon.png")}
					transition={10}
					onLoad={() => setImageLoaded(true)}
				/>
			</View>

			<TouchableOpacity
				onPress={() => {
					router.replace("/login");
				}}
				style={styles.button}
			>
				<Text style={styles.buttonOutlineText}>Start the Journey</Text>
			</TouchableOpacity>
		</View>
	);
};

const styles = StyleSheet.create({
	beginContainer: {
		flex: 1,
		justifyContent: "flex-start",
		alignItems: "center",
		paddingTop: 150,
	},
	logoContainer: {
		marginBottom: 20,
		width: 300,
		height: 300,
	},
	logo: {
		width: "100%",
		height: "100%",
	},
	button: {
		backgroundColor: Colors.standartAppColor,
		paddingVertical: 15,
		paddingHorizontal: 30,
		borderRadius: 10,
		borderColor: "#0782F9",
		borderWidth: 2,
	},
	buttonOutlineText: {
		color: "white",
		fontWeight: "700",
		fontSize: 24,
	},
});

export default Index;
