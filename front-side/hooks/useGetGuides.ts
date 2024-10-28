import { BASE_URL } from "@/constants/request-api-constants";
import axios from "axios";

export const useGetGuides = async () => {
  const response = await axios.get(BASE_URL + "");
  return response.data;
};
