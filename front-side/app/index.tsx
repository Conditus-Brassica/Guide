import { FirebaseAuth } from "@/FirebaseConfig";
import { router } from "expo-router";
import React, { useEffect, useState } from "react";
import { StyleSheet, View, Text } from "react-native";
import { TouchableOpacity } from "react-native-gesture-handler";

const Index = () => {
	return (
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
	);
};

const styles = StyleSheet.create({
	container: {
		flex: 1,
	},
	button: {
		backgroundColor: "white",
		marginTop: 5,
		borderColor: "#0782F9",
		borderWidth: 2,
		alignItems: "center",
		justifyContent: "center",
	},
	buttonOutlineText: { color: "blue", fontWeight: "700", fontSize: 32 },
});

export default Index;
