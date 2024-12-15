import { LatLng } from "react-native-maps";

export type landmarkInfo = {
	_id: string;
	_source: LandmarkSearchDetails;
};

type LandmarkSearchDetails = {
	name: string;
	coordinates: LatLng;
};

export type RecommendationInfo = {
	recommendation: Recommendation[];
};

export type Recommendation = {
	name: string;
	latitude: number;
	longitude: number;
	row_index: number;
	row_uuid: string;
};
