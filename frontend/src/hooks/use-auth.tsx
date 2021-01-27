import React, {ComponentProps, createContext, useContext, useState} from "react";
import {authenticate, User} from "../lib/auth";

type Maybe<T> = T | undefined;

type AuthContext = {
  user?: User,
  login: (token: string) => Promise<User>,
  isLoggedIn: () => boolean,
  logout: () => void
};

const emptyAuthContext: AuthContext = {
  login: _ => Promise.reject(),
  isLoggedIn: () => false,
  logout: () => {
  }
};

const authContext = createContext<AuthContext>(emptyAuthContext);

export function AuthProvider({children}: ComponentProps<any>) {
  const auth = useProvideAuth();
  return <authContext.Provider value={auth}>{children}</authContext.Provider>;
}

export const useAuth = () => {
  return useContext(authContext);
};

function useProvideAuth(): AuthContext {

  const [user, setUser] = useState<Maybe<User>>(undefined);

  const login = async (token: string) => {
    const {user} = await authenticate(token);
    setUser(user);
    console.log("Set user", user);
    return user;
  };

  const isLoggedIn = () => {
    return !!user;
  };

  const logout = () => {
    setUser(undefined);
  };


  return {user, login, isLoggedIn, logout};

}

