import {
	DarkTheme,
	DefaultTheme,
	ThemeProvider,
} from "@react-navigation/native";
import { useFonts } from "expo-font";
import { Stack } from "expo-router";
import * as SplashScreen from "expo-splash-screen";
import { useEffect, useState } from "react";
import "react-native-reanimated";

import { setStatusBarHidden, StatusBar } from "expo-status-bar";

// Prevent the splash screen from auto-hiding before asset loading is complete.
SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
	const [loaded] = useFonts({
		SpaceMono: require("../assets/fonts/SpaceMono-Regular.ttf"),
	});

	useEffect(() => {
		if (loaded) {
			SplashScreen.hideAsync();
		}
	}, [loaded]);

	if (!loaded) {
		return null;
	}

	return (
		<ThemeProvider value={DarkTheme}>
			<StatusBar hidden={true} />
			<Stack>
				<Stack.Screen
					name="index"
					options={{
						headerShown: false,
						statusBarHidden: true,
					}}
				/>
				<Stack.Screen
					name="login"
					options={{
						headerShown: false,
						statusBarHidden: true,
					}}
				/>
				<Stack.Screen
					name="home/(tabs)"
					options={{
						statusBarHidden: true,
					}}
				/>
				<Stack.Screen name="+not-found" />
			</Stack>
		</ThemeProvider>
	);
}
