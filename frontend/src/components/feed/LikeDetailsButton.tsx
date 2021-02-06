import React from "react";
import {useHistory} from "react-router-dom";

function choosePlural(likeCount: number, singular: string, plural: string) {
  return likeCount === 1 ? singular : plural;
}

type LikeDetailsButtonProps = { count: number, appreciationId: number }

export default function LikeDetailsButton({count, appreciationId}: LikeDetailsButtonProps) {
  const history = useHistory();
  const handleOnClick = () => history.push(`/appreciation/${appreciationId}/likes`);

  return (
    <button type="button" className="clear-button has-text-danger level-item is-clickable" onClick={handleOnClick}>
      <span>{count} {choosePlural(count, 'like', 'likes')}</span>
    </button>);
}
