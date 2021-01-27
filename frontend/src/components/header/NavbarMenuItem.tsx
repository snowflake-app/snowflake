import {NavLink, NavLinkProps} from "react-router-dom";
import React from "react";

export default function NavbarMenuItem({icon, label, ...linkProps}: NavLinkProps & { icon: string, label: string }) {
  return (
    <NavLink {...linkProps} activeClassName="is-active" className="navbar-item">
      <span className="icon is-medium">
          <ion-icon class="is-size-5" name={icon}/>
      </span>
      <span>{label}</span>
    </NavLink>);
}
