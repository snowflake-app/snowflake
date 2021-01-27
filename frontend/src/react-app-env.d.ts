/// <reference types="react-scripts" />
import React from "react";

declare global {
  namespace JSX {
    // noinspection JSUnusedGlobalSymbols
    interface IntrinsicElements {
      'ion-icon': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement> & { name: string, size?: string }; // Normal web component
    }
  }
}
