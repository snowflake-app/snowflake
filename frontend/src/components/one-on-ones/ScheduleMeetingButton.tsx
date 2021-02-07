import React from "react";

export default function ScheduleMeetingButton({title}: { title: string }) {
    return (
        <a className="button is-medium is-primary"
           href={`https://www.google.com/calendar/render?action=TEMPLATE&text=${encodeURIComponent(title)}`}>
      <span className="icon is-medium">
        <ion-icon size="large" name="calendar-outline"/>
      </span>
            <span>Schedule</span>
        </a>)
}
