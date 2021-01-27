import {useAuth} from "../../hooks/use-auth";
import {Link} from "react-router-dom";
import React from "react";

export default function ProfileDropdownMenu() {
    const auth = useAuth();

    return <div className="navbar-item has-dropdown is-hoverable">
        <Link to="/" className="navbar-link">Hello {auth.user?.name}</Link>

        <div className="navbar-dropdown is-right">
            <Link to="/" className="navbar-item">
              <span className="icon">
                <ion-icon size="large" name="person-circle-outline"/>
              </span><span>
                Profile
              </span>
            </Link>
            <hr className="navbar-divider"/>
            <Link to="/" className="navbar-item">
                <span className="icon">
                  <ion-icon size="large" name="help-circle-outline"/>
                </span><span>
                  Help
                </span>
            </Link>
            <hr className="navbar-divider"/>
            <Link to="/" className="navbar-item">
                  <span className="icon">
                    <ion-icon size="large" name="exit-outline"/>
                  </span><span>
                    Sign out
                  </span>
            </Link>
        </div>
    </div>;
}
