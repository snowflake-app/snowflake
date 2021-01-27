import {token} from "./auth";

export function authorizationHeaders() {
  return {
    'Authorization': `Bearer ${token()}`
  }
}
