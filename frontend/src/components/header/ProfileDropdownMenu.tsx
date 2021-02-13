import {useAuth} from "../../hooks/use-auth";
import {Link, useHistory} from "react-router-dom";
import React from "react";
import styles from './ProfileDropdownMenu.module.css';

export default function ProfileDropdownMenu() {
  const {user, logout} = useAuth();
  const history = useHistory();

  const {name, username} = user!;

  const signOut = () => {
    logout();
    history.push("/");
  };

  return (
    <div className="navbar-item has-dropdown is-hoverable">
      <Link to={`/profile/${username}`} className="navbar-link">Hello {name}</Link>

      <div className="navbar-dropdown is-right">
        <Link to={`/profile/${username}`} className="navbar-item is-align-items-center">
          <span className={`icon ${styles.icon}`}>
            <ion-icon size="large" name="person-circle-outline"/>
          </span>
          <span>
            Profile
          </span>
        </Link>
        <hr className="navbar-divider"/>
        {/*<Link to="/" className="navbar-item is-align-items-center">*/}
        {/*  <span className={`icon ${styles.icon}`}>*/}
        {/*    <ion-icon size="large" name="help-circle-outline"/>*/}
        {/*  </span>*/}
        {/*  <span>*/}
        {/*    Help*/}
        {/*  </span>*/}
        {/*</Link>*/}
        {/*<hr className="navbar-divider"/>*/}
        <Link to="/" onClick={signOut} className="navbar-item is-align-items-center">
          <span className={`icon ${styles.icon}`}>
            <ion-icon size="large" name="exit-outline"/>
          </span>
          <span>Sign out</span>
        </Link>
      </div>
    </div>);
}
