import React from 'react';
import LoginPage from "./LoginPage";
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
            <Route path="/login">
              <LoginPage/>
            </Route>
            <ProtectedRoute exact={true} path="/">
              <Snowflake/>
            </ProtectedRoute>
          </Switch>
        </BrowserRouter>
      </AuthProvider>
    </AlertProvider>
  )
    ;
}
