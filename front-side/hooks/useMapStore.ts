import { create } from "zustand";

export const useMapStore = create(() => ({
  initialPosition: {
    latitude: 53.893009,
    longitude: 27.567444,
    latitudeDelta: 0.5,
    longitudeDelta: 0.2,
  },
}));
