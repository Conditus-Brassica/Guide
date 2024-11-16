import { FirebaseAuth } from "@/FirebaseConfig";
import { router } from "expo-router";
import { signOut } from "firebase/auth";
import { StyleSheet, Text, View, TouchableOpacity } from "react-native";

const Profile = () => {
	const HandleSignOut = () => {
		signOut(FirebaseAuth)
			.then(() => router.replace("/login"))
			.catch((error: Error): void => alert(error.message));
	};

	return (
		<View style={styles.container}>
			<Text style={{ color: "white" }}>Your own profile!</Text>
			<TouchableOpacity style={styles.button} onPress={HandleSignOut}>
				<Text style={styles.buttonText}>Sign out</Text>
			</TouchableOpacity>
		</View>
	);
};

const styles = StyleSheet.create({
	container: {
		flex: 1,
		justifyContent: "flex-end",
		alignItems: "center",
	},
	button: {
		backgroundColor: "black",
		marginTop: 5,
		padding: 15,
		borderColor: "#769dac",
		borderWidth: 2,
		alignItems: "center",
		justifyContent: "center",
		width: "100%",
	},
	buttonText: { color: "white", fontWeight: "700", fontSize: 16 },
});

export default Profile;
