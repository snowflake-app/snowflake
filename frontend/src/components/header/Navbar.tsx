import {Link} from "react-router-dom";
import React from "react";
import ProfileDropdownMenu from "./ProfileDropdownMenu";
import NavbarMenuItem from "./NavbarMenuItem";
import {Notifications} from "./Notifications";

export default function Navbar() {
  return (
    <nav className="navbar is-fixed-top" role="navigation" aria-label="main navigation">
      <div className="navbar-brand">
        <Link className="navbar-item" to="/">
          <span className="icon has-text-primary is-large">
            <ion-icon size="large" name="snow-outline"/>
          </span>
          <span className="title">Snowflake</span>
        </Link>
        <button className="navbar-burger burger" aria-label="menu" aria-expanded="false"
                data-target="menu">
          <span aria-hidden="true"/>
          <span aria-hidden="true"/>
          <span aria-hidden="true"/>
        </button>
      </div>

      <div id="menu" className="navbar-menu hide">
        <div className="navbar-start">
        </div>

        <div className="navbar-end">
          <NavbarMenuItem to="/feed" icon="home-outline" label="Feed"/>
          <NavbarMenuItem to="/1-on-1s" icon="people-outline" label="1-on-1s"/>
          <NavbarMenuItem to="/personal-objectives" icon="rocket-outline" label="Personal objectives"/>
          <Notifications/>
          <ProfileDropdownMenu/>
        </div>
      </div>
    </nav>);
}
