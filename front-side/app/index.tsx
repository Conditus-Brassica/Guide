import { router } from "expo-router";
import React from "react";
import { StyleSheet, View, Text, TouchableOpacity } from "react-native";

const Index = () => {
	return (
		<View style={styles.beginContainer}>
			<View style={styles.logoContainer}>
				<Text style={styles.logo}>GUIDE</Text>
			</View>
			<View style={styles.container}>
				<TouchableOpacity
					onPress={() => {
						router.replace("/login");
					}}
					style={styles.button}
				>
					<Text style={styles.buttonOutlineText}>Start the Journey</Text>
				</TouchableOpacity>
			</View>
		</View>
	);
};

const styles = StyleSheet.create({
	beginContainer: {
		flex: 1,
		flexDirection: "column",
	},
	logoContainer: { flex: 0.5, alignItems: "center", justifyContent: "center" },
	container: {
		flex: 2,
		alignItems: "center",
		justifyContent: "center",
	},
	button: {
		backgroundColor: "white",
		padding: 15,
		borderRadius: 10,
		borderColor: "#0782F9",
		borderWidth: 2,
	},
	logo: {
		fontSize: 70,
		alignItems: "center",
		fontStyle: "italic",
		fontWeight: "700",
		color: "#769dac",
		marginTop: 1,
		justifyContent: "center",
		padding: 10,
	},
	buttonOutlineText: { color: "blue", fontWeight: "700", fontSize: 32 },
});

export default Index;
