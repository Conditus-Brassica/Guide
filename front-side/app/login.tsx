import { FirebaseAuth } from "@/FirebaseConfig";
import { router } from "expo-router";
import { StatusBar } from "expo-status-bar";
import {
	createUserWithEmailAndPassword,
	signInWithEmailAndPassword,
} from "firebase/auth";
import { useEffect, useState } from "react";
import {
	KeyboardAvoidingView,
	Text,
	View,
	StyleSheet,
	TouchableOpacity,
	TextInput,
} from "react-native";

// This is done step by step like in guide, so I'm not so good as you think
const LoginScreen = () => {
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");

	const handleSignup = () => {
		createUserWithEmailAndPassword(FirebaseAuth, email, password)
			.then()
			.catch((error) => alert(error.message));
	};

	const handleLogin = () => {
		signInWithEmailAndPassword(FirebaseAuth, email, password)
			.then()
			.catch((error) => alert(error.message));
	};

	useEffect(() => {
		const unsubscribe = FirebaseAuth.onAuthStateChanged((user) => {
			if (user) {
				router.replace("/home/(tabs)/home");
			}

			return unsubscribe;
		});
	});

	return (
		<KeyboardAvoidingView behavior="padding" style={styles.container}>
			<StatusBar hidden={true} />
			<View style={styles.inputContainer}>
				<TextInput
					placeholder="Login"
					value={email}
					onChangeText={(text) => setEmail(text)}
					style={styles.input}
				/>
				<TextInput
					placeholder="Password"
					value={password}
					onChangeText={(text) => setPassword(text)}
					style={styles.input}
					secureTextEntry
				/>
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
		borderRadius: 10,
		marginTop: 5,
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

export default LoginScreen;
