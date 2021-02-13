import {useReducer} from "react";

export function useToggle(initialValue = false) {
  return useReducer((state) => !state, initialValue);
}
