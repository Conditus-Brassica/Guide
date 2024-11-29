import { FirebaseAuth } from "@/FirebaseConfig";
import { router } from "expo-router";
import { signOut, updateProfile } from "firebase/auth";
import { StyleSheet, Text, View, TouchableOpacity } from "react-native";
import { Avatar } from "@rneui/themed";
import { Colors } from "@/constants/Colors";
import { useEffect, useState } from "react";
import * as ImagePicker from "expo-image-picker";

const Profile = () => {
	const user = FirebaseAuth.currentUser;
	const [image, setImage] = useState<string | null>(user?.photoURL ?? null);

	const pickImage = async () => {
		let result = await ImagePicker.launchImageLibraryAsync({
			mediaTypes: ["images", "videos"],
			allowsEditing: true,
			aspect: [4, 3],
			quality: 1,
		});

		if (!result.canceled) {
			setImage(result.assets[0].uri);
			await updateProfile(user!!, { photoURL: result.assets[0].uri });
		}
	};

	const HandleSignOut = () => {
		signOut(FirebaseAuth)
			.then(() => router.replace("/login"))
			.catch((error: Error): void => alert(error.message));
	};
	return (
		<View style={{ flex: 1 }}>
			<View style={styles.emailContainer}>
				<Avatar
					containerStyle={styles.avatar}
					size={64}
					rounded
					source={{ uri: image ?? require("@/assets/images/app-icon.png") }}
				>
					<Avatar.Accessory size={23} onPress={pickImage} />
				</Avatar>
				<Text
					style={{ color: "white", fontSize: 24 }}
					children={"Email: " + user?.email}
				/>
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
	emailContainer: {
		flex: 3,
		alignItems: "center",
		justifyContent: "flex-start",
		marginTop: 35,
	},
	container: {
		flex: 1,
		justifyContent: "flex-end",
		alignItems: "center",
	},
	avatar: { backgroundColor: Colors.standartAppColor },
	button: {
		backgroundColor: "white",
		marginTop: 5,
		padding: 15,
		borderColor: Colors.standartAppColor,
		borderWidth: 2,
		alignItems: "center",
		justifyContent: "center",
		width: "100%",
	},
	buttonText: { color: "black", fontWeight: "700", fontSize: 16 },
});

export default Profile;
