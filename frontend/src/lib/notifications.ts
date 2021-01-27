import axios from "axios";
import {authorizationHeaders} from "./utils";

export async function notificationCount() {
  const response = await axios.get("/api/notifications/_count", {
    headers: authorizationHeaders()
  });

  return response.data
}
