import React, {FormHTMLAttributes} from "react";

export default function AppreciationForm({className, ...props}: FormHTMLAttributes<HTMLFormElement>) {
  return <form {...props} className={`note-form block ${className}`}>
    <div className="field">
      <label htmlFor=" note-field" className="is-sr-only">Write a note a @mention to send a note</label>
      <div className="control">
        <textarea rows={2} className="textarea" placeholder="Write a message that includes @mention"/>
      </div>
    </div>
    <div className="field mt-2 send-container is-clipped">
      <div className="control">
        <button className="button is-primary is-rounded is-medium">
          <span className="icon">
            <ion-icon name="paper-plane-outline" size=" large"/>
          </span>
          <span>Hi five!</span>
        </button>
      </div>
    </div>
  </form>;
}
