import { LatLng, Region } from "react-native-maps";
import { create } from "zustand";

type MapStore = {
	initialPosition: Region;
	activeRoute: RouteType | null;
	setInitialCoords: (coords: LatLng) => void;
	setActiveRoute: (coords: RouteType) => void;
};

type RouteType = {
	origin: LatLng;
	destination: LatLng;
};

export const useMapStore = create<MapStore>((set) => ({
	initialPosition: {
		latitude: 53.893009,
		longitude: 27.567444,
		latitudeDelta: 0.5,
		longitudeDelta: 0.2,
	},
	activeRoute: null,
	setInitialCoords: (coords) =>
		set((state) => ({
			initialPosition: {
				...state.initialPosition, // Keep existing `latitudeDelta` and `longitudeDelta`
				latitude: coords.latitude,
				longitude: coords.longitude,
			},
		})),
	setActiveRoute: (coords) => set(() => ({ activeRoute: coords })),
}));
