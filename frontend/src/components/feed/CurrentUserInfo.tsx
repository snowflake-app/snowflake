import {useAuth} from "../../hooks/use-auth";
import React from "react";
import UserInfo from "../UserInfo";

export default function CurrentUserInfo() {
  const {user} = useAuth();
  return user ? <UserInfo {...user} /> : <span>Logged out</span>;
}
