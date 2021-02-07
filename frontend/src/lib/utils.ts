import {token, User} from "./auth";

export function authorizationHeaders() {
  return {
    'Authorization': `Bearer ${token()}`
  }
}

export function isCreatedByUser(object: { createdBy?: User }, user?: User) {
  return user?.username === object.createdBy?.username;
}
