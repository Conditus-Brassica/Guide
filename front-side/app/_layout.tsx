import {
	DarkTheme,
	DefaultTheme,
	ThemeProvider,
} from "@react-navigation/native";
import { useFonts } from "expo-font";
import { Stack } from "expo-router";
import * as SplashScreen from "expo-splash-screen";
import { useEffect } from "react";
import "react-native-reanimated";

import { StatusBar } from "expo-status-bar";
import { useAssets } from "expo-asset";

SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
	const [loaded] = useFonts({
		SpaceMono: require("../assets/fonts/SpaceMono-Regular.ttf"),
	});

	const [loadedAssets] = useAssets([
		require("./../assets/images/app-icon.png"),
	]);

	useEffect(() => {
		if (loaded && loadedAssets) {
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
					name="home/articles/[id]"
					options={{
						headerTitle: "Article",
					}}
				/>
				<Stack.Screen
					name="index"
					options={{
						headerShown: false,
					}}
				/>
				<Stack.Screen
					name="login"
					options={{
						headerShown: false,
					}}
				/>
				<Stack.Screen
					name="home/(tabs)"
					options={{
						headerShown: false,
					}}
				/>
				<Stack.Screen name="+not-found" />
			</Stack>
		</ThemeProvider>
	);
}
