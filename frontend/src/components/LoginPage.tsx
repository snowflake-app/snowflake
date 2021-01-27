import React from "react";
import {GoogleLogin} from 'react-google-login';

import styles from './LoginPage.module.css';
import {useHistory, useLocation} from "react-router-dom";
import {useAlerts} from "../hooks/use-alerts";
import googleLogo from "../images/google-logo.svg";
import {useAuth} from "../hooks/use-auth";

export default function LoginPage() {
  const history = useHistory();
  const location = useLocation();

  const {addAlert} = useAlerts();
  const {login} = useAuth();


  const doLogin = async (data: any) => {
    console.log(data);

    const idToken = data.getAuthResponse().id_token;

    try {
      await login(idToken);

      const params = new URLSearchParams(location.search);
      const next = params.get('next') || '/';
      history.replace({pathname: next});
    } catch (e) {
      addAlert({
        category: "danger",
        title: 'Error',
        content: e.message
      })
    }
  };

  const loginError = (data: any) => {
    console.log(data);
    addAlert({
      category: "danger",
      title: 'Error',
      content: 'Error authenticating with Google'
    });
  };

  // noinspection CheckTagEmptyBody
  return (
    <div className={styles.loginPage}>
      <div className="box has-text-centered p-6">
        <p className="is-size-1 mb-4 has-text-primary">
          <ion-icon name="snow-outline"></ion-icon>
        </p>
        <h1 className="title">Welcome to Snowflake!</h1>
        <p className="subtitle block my-4">You can sign in with SSO, using your work email address</p>
        <form method="post" className="field mt-6">
          <div className="control">
            <GoogleLogin
              className="button is-large is-light"
              clientId={'' + process.env.REACT_APP_GOOGLE_CLIENT_ID}
              onSuccess={doLogin}
              onFailure={loginError}
              cookiePolicy="single_host_origin"
              render={renderProps => (
                <button className="button is-large is-light" onClick={renderProps.onClick}
                        disabled={renderProps.disabled}>
                  <div className="mr-1 p-1">
                    <img alt="Google logo" src={googleLogo}/>
                  </div>
                  Sign in with Google
                </button>
              )}
            />
          </div>
        </form>
      </div>
    </div>
  );
}
