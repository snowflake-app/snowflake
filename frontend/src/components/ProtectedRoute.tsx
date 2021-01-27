import React from "react";
import {Redirect, Route, RouteProps} from "react-router-dom";
import {useAuth} from "../hooks/use-auth";

export default function ProtectedRoute({children, ...rest}: RouteProps) {
  const {isLoggedIn} = useAuth();

  return (
    <Route
      {...rest}
      render={({location}) => {
        if (isLoggedIn()) {
          return (children);
        }

        return <Redirect
          to={{
            pathname: `/login`,
            search: `?next=${location.pathname}`
          }}
        />;
      }}
    />
  );
}
