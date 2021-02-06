import {Like} from "../../lib/api";
import React, {ButtonHTMLAttributes} from "react";

type LikeButtonProps = { like: Like } & ButtonHTMLAttributes<HTMLButtonElement>

export default function LikeButton({like, onClick}: LikeButtonProps) {
  return (
    <button title="Like" type="button"
            onClick={onClick}
            className="post-action-button clear-button has-text-danger level-item is-clickable">
      <span className="icon is-medium">
        <ion-icon name={like ? 'heart' : 'heart-outline'}/>
      </span>
    </button>
  );
}
