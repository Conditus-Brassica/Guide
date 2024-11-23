import { FirebaseAuth } from "@/FirebaseConfig";
import { router } from "expo-router";
import { signOut } from "firebase/auth";
import { StyleSheet, Text, View, TouchableOpacity } from "react-native";

const Profile = () => {
	const user = FirebaseAuth.currentUser;

	const HandleSignOut = () => {
		signOut(FirebaseAuth)
			.then(() => router.replace("/login"))
			.catch((error: Error): void => alert(error.message));
	};

	return (
		<View>
			<View style={styles.emailContainer}>
				<Text style={{ color: "white", fontSize: 24 }} children={user?.email} />
			</View>
			<View style={styles.container}>
				<TouchableOpacity style={styles.button} onPress={HandleSignOut}>
					<Text style={styles.buttonText}>Sign out</Text>
				</TouchableOpacity>
			</View>
		</View>
	);
};

const styles = StyleSheet.create({
	emailContainer: { flex: 1, justifyContent: "center", alignItems: "center" },
	container: {
		flex: 0.3,
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
