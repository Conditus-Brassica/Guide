import { LatLng } from "react-native-maps";

export type landmarkInfo = {
	_id: string;
	_source: LandmarkSearchDetails;
};

type LandmarkSearchDetails = {
	name: string;
	coordinates: LatLng;
};
