import { Colors } from "@/constants/Colors";
import { BASE_URL } from "@/constants/request-api-constants";
import { FirebaseAuth } from "@/FirebaseConfig";
import axios from "axios";
import { router } from "expo-router";
import { StatusBar } from "expo-status-bar";
import {
	createUserWithEmailAndPassword,
	signInWithEmailAndPassword,
} from "firebase/auth";
import React, { useEffect, useState } from "react";
import {
	KeyboardAvoidingView,
	Text,
	View,
	StyleSheet,
	TouchableOpacity,
} from "react-native";
import { HelperText, TextInput } from "react-native-paper";

export type UserInfo = {
	userId: string;
};

type ErrorType = {
	[key: string]: string;
};

const LoginScreen = () => {
	const [form, setForm] = useState({ email: "", password: "" });
	const [errors, setErrors] = useState<ErrorType>({});

	const postUserInfo = () => {
		try {
			const user = FirebaseAuth.currentUser;
			axios.post<UserInfo>(BASE_URL, { email: user?.uid });
		} catch (error) {
			console.error(`HTTP request error: ${error}`);
		}
	};

	const handleSignup = async () => {
		try {
			await createUserWithEmailAndPassword(
				FirebaseAuth,
				form.email,
				form.password
			);
			postUserInfo();
			setErrors({});
		} catch (error: any) {
			const parsedErrors = parseFirebaseError(error);
			setErrors(parsedErrors);
		}
	};

	const handleLogin = async () => {
		try {
			await signInWithEmailAndPassword(FirebaseAuth, form.email, form.password);
			setErrors({});
		} catch (error: any) {
			const parsedErrors = parseFirebaseError(error);
			setErrors(parsedErrors);
		}
	};

	const handleFormChange = (key: string, value: string) => {
		setForm((prev) => ({ ...prev, [key]: value }));
	};

	useEffect(() => {
		const unsubscribe = FirebaseAuth.onAuthStateChanged((user) => {
			if (user) {
				router.replace("/home/(tabs)/home");
			}
			return () => unsubscribe();
		});
	});

	return (
		<KeyboardAvoidingView behavior="padding" style={styles.container}>
			<View style={styles.inputContainer}>
				<TextInput
					placeholder="Email"
					value={form.email}
					style={styles.input}
					onChangeText={(text) => {
						handleFormChange("email", text);
						setErrors({});
					}}
				/>
				<HelperText
					style={{ color: "red" }}
					type="error"
					visible={!!errors.email}
				>
					{errors.email}
				</HelperText>
				<TextInput
					placeholder="Password"
					value={form.password}
					onChangeText={(text) => {
						handleFormChange("password", text);
						setErrors({});
					}}
					style={styles.input}
					secureTextEntry
				/>
				<HelperText
					style={{ color: "red" }}
					type="error"
					visible={!!errors.password}
				>
					{errors.password}
				</HelperText>
			</View>
			<View style={styles.buttonContainter}>
				<TouchableOpacity onPress={handleLogin} style={styles.button}>
					<Text>Login</Text>
				</TouchableOpacity>
				<TouchableOpacity
					onPress={handleSignup}
					style={[styles.button, styles.buttonOutline]}
				>
					<Text style={styles.buttonOutlineText}>Register</Text>
				</TouchableOpacity>
			</View>
		</KeyboardAvoidingView>
	);
};

const styles = StyleSheet.create({
	container: {
		flex: 1,
		justifyContent: "center",
		alignItems: "center",
	},
	inputContainer: { width: "80%" },
	input: {
		backgroundColor: "white",
		paddingHorizontal: 15,
		paddingVertical: 10,
		borderTopLeftRadius: 15,
		borderTopRightRadius: 15,
		borderBottomLeftRadius: 15,
		borderBottomRightRadius: 15,
		marginTop: 5,
		borderWidth: 1,
		borderColor: Colors.standartAppColor,
	},
	labels: { fontWeight: "bold" },
	buttonContainter: {
		width: "60%",
		justifyContent: "center",
		alignItems: "center",
		marginTop: 40,
	},
	button: {
		backgroundColor: "#44c1ff",
		width: "100%",
		padding: 15,
		borderRadius: 10,
		alignItems: "center",
	},
	buttonOutline: {
		backgroundColor: "white",
		marginTop: 5,
		borderColor: "#44c1ff",
		borderWidth: 2,
		padding: 10,
	},
	buttonText: { color: "white", fontWeight: "700", fontSize: 16 },
	buttonOutlineText: { color: "blue", fontWeight: "700", fontSize: 16 },
});

const parseFirebaseError = (error: any): ErrorType => {
	const errorType: ErrorType = {};

	// Handle specific Firebase Auth error codes
	switch (error.code) {
		case "auth/email-already-in-use":
			errorType.email = "Email is already in use.";
			break;
		case "auth/invalid-email":
			errorType.email = "Invalid email address.";
			break;
		case "auth/user-not-found":
			errorType.email = "No user found with this email.";
			break;
		case "auth/wrong-password":
			errorType.password = "Incorrect password.";
			break;
		case "auth/weak-password":
			errorType.password = "Password is too weak.";
			break;
		default:
			errorType.general = "An unknown error occurred. Please try again.";
	}

	return errorType;
};

export default LoginScreen;
