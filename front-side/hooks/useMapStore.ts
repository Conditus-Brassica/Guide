import { LatLng, Region } from "react-native-maps";
import { create } from "zustand";

type MapStore = {
	initialPosition: Region;
	activeRoute: RouteType | null;
	setInitialCoords: (coords: Region) => void;
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
	setInitialCoords: (coords) => set(() => ({ initialPosition: coords })),
	setActiveRoute: (coords) => set(() => ({ activeRoute: coords })),
}));
