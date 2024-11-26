import { FirebaseAuth } from "@/FirebaseConfig";
import { router } from "expo-router";
import { signOut } from "firebase/auth";
import { StyleSheet, Text, View, TouchableOpacity } from "react-native";
//Rewrute this element completely
const Profile = () => {
	const user = FirebaseAuth.currentUser;

	const HandleSignOut = () => {
		signOut(FirebaseAuth)
			.then(() => router.replace("/login"))
			.catch((error: Error): void => alert(error.message));
	};
	console.log(user);
	return (
		<View style={{ flex: 1 }}>
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
	emailContainer: { flex: 1 },
	container: {
		flex: 0.3,
		justifyContent: "flex-end",
		alignItems: "center",
	},
	button: {
		backgroundColor: "grey",
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
