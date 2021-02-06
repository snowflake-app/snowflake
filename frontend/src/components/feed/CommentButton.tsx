import React from "react";

type CommentButtonProps = { count: number } & React.ButtonHTMLAttributes<HTMLButtonElement>

export default function CommentButton({count, ...props}: CommentButtonProps) {
  return (
    <button title="Comment"
            className="post-action-button comment-button clear-button has-text-info level-item is-clickable"
            {...props}>
          <span className="icon is-medium">
            <ion-icon name="chatbubble-outline"/>
          </span>
      <span>{count}</span>
    </button>);
}
