import { FirebaseAuth } from "@/FirebaseConfig";
import { router } from "expo-router";
import { signOut, updateProfile } from "firebase/auth";
import { StyleSheet, Text, View, TouchableOpacity, Alert } from "react-native";
import { Avatar, Card, Icon, ListItem } from "@rneui/themed";
import { Colors } from "@/constants/Colors";
import { useEffect, useState } from "react";
import * as ImagePicker from "expo-image-picker";
import { TextInput } from "react-native-paper";
import AsyncStorage from "@react-native-async-storage/async-storage";
import {
	storageUserEmailKey,
	storageUserPasswordKey,
} from "@/constants/async-storage-constants";

const Profile = () => {
	const user = FirebaseAuth.currentUser;
	const [image, setImage] = useState<string | null>(user?.photoURL ?? null);
	const [isEditing, setIsEditing] = useState(false);
	const [newDisplayName, setNewDisplayName] = useState(user?.displayName ?? "");

	const pickImage = async () => {
		let result = await ImagePicker.launchImageLibraryAsync({
			mediaTypes: ["images"],
			allowsEditing: true,
			aspect: [4, 3],
			quality: 1,
		});

		if (!result.canceled) {
			setImage(result.assets[0].uri);
			await updateProfile(user!, { photoURL: result.assets[0].uri });
		}
	};

	const handleUpdateDisplayName = async () => {
		try {
			if (newDisplayName.trim() === "") {
				Alert.alert("Error", "Display name cannot be empty.");
				return;
			}
			await updateProfile(user!, { displayName: newDisplayName });
			Alert.alert("Success", "Display name updated successfully.");
			setIsEditing(false);
		} catch (error) {
			console.error("Failed to update display name:", error);
			Alert.alert("Error", "Failed to update display name. Please try again.");
		}
	};

	const HandleSignOut = () => {
		AsyncStorage.multiRemove([storageUserEmailKey, storageUserPasswordKey]);
		signOut(FirebaseAuth)
			.then(() => router.replace("/login"))
			.catch((error: Error): void => alert(error.message));
	};
	return (
		<View style={{ flex: 1 }}>
			<View style={styles.emailContainer}>
				<Card
					containerStyle={{
						justifyContent: "flex-start",
						borderRadius: 15,
						borderColor: Colors.standartAppColor,
						borderWidth: 2,
						backgroundColor: "#444444",
					}}
				>
					<View style={styles.cardHeader}>
						{isEditing ? (
							<TextInput
								label="Name"
								mode="flat"
								value={newDisplayName}
								onChangeText={setNewDisplayName}
								outlineColor={Colors.standartAppColor}
								activeOutlineColor={Colors.standartAppColor}
								style={{
									flex: 1,
									marginRight: 10,
								}}
								placeholder="Enter new name"
								autoComplete="name"
							/>
						) : (
							<Card.Title style={{ flex: 1, marginLeft: 25, color: "white" }}>
								{user?.displayName}
							</Card.Title>
						)}
						<Icon
							name={isEditing ? "check" : "edit"}
							type="material"
							size={20}
							color="gray"
							onPress={() => {
								if (isEditing) {
									handleUpdateDisplayName();
								} else {
									setIsEditing(true);
								}
							}}
						/>
					</View>
					<Card.Divider />
					<Avatar
						containerStyle={styles.avatar}
						size="large"
						rounded
						source={{ uri: image ?? require("@/assets/images/app-icon.png") }}
					>
						<Avatar.Accessory size={23} onPress={pickImage} />
					</Avatar>
					<ListItem
						containerStyle={{ backgroundColor: Colors.standartAppGrey }}
					>
						<ListItem.Content>
							<ListItem.Title style={{ color: "white" }}>Email</ListItem.Title>
							<ListItem.Subtitle style={{ color: "white" }}>
								{user?.email}
							</ListItem.Subtitle>
						</ListItem.Content>
					</ListItem>
					<TouchableOpacity style={styles.button} onPress={HandleSignOut}>
						<Text style={styles.buttonText}>Sign out</Text>
					</TouchableOpacity>
				</Card>
			</View>
		</View>
	);
};

const styles = StyleSheet.create({
	cardHeader: {
		flexDirection: "row",
		justifyContent: "space-between",
		width: "100%",
		alignItems: "center",
	},
	emailContainer: {
		flex: 1,
		marginTop: 35,
	},
	container: {
		flex: 1,
		justifyContent: "flex-end",
		alignItems: "center",
	},
	avatar: { backgroundColor: Colors.standartAppColor, alignSelf: "center" },
	button: {
		backgroundColor: "white",
		marginTop: 5,
		padding: 15,
		borderColor: Colors.standartAppColor,
		borderWidth: 2,
		alignItems: "center",
		justifyContent: "center",
		alignSelf: "flex-end",
		width: "100%",
	},
	buttonText: { color: "black", fontWeight: "700", fontSize: 16 },
});

export default Profile;
