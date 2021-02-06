import {useEffect, useRef} from "react";

export function useEventListener(event: string, handler: EventListener, element: EventTarget = document) {
  const savedHandler = useRef<EventListener>();

  useEffect(() => {
    savedHandler.current = handler;
  }, [handler]);

  useEffect(
    () => {
      const listener = (event: Event) => {
        if (savedHandler.current) {
          savedHandler.current(event);
        }
      };

      element.addEventListener(event, listener);

      return () => {
        element.removeEventListener(event, listener);
      };
    },
    [event, element]
  );
}
