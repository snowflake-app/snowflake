import React from "react";

import {useAsync} from "../../hooks/use-async";
import {appreciations} from "../../lib/api";
import Loading from "../Loading";
import Appreciation from "./Appreciation";

export function Appreciations() {
  const {status, value} = useAsync(appreciations);

  return (
    <>
      {status === 'pending' && <Loading/>}
      {status === "success" && value?.map(appreciation => (
        <Appreciation key={appreciation.id} {...appreciation} />))
      }
    </>);
}
