import React from 'react';
import LoginPage from "./login/LoginPage";
import Snowflake from "./Snowflake";
import ProtectedRoute from "./ProtectedRoute";
import {BrowserRouter, Route, Switch} from "react-router-dom";
import {AuthProvider} from "../hooks/use-auth";
import {AlertProvider} from "../hooks/use-alerts";
import AlertContainer from "./AlertContainer";

export default function App() {
  return (
    <AlertProvider>
      <AlertContainer/>
      <AuthProvider>
        <BrowserRouter>
          <Switch>
            <Route exact={true} path="/login">
              <LoginPage/>
            </Route>
            <ProtectedRoute path="/">
              <Snowflake/>
            </ProtectedRoute>
          </Switch>
        </BrowserRouter>
      </AuthProvider>
    </AlertProvider>
  )
    ;
}
