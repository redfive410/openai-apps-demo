import { useEffect, useState } from "react";
import type { WidgetProps } from "./types";

export function useWidgetProps<T = any>(): WidgetProps<T> {
  const [props, setProps] = useState<WidgetProps<T>>({});

  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      if (event.data?.type === "widget-props") {
        setProps(event.data.props || {});
      }
    };

    window.addEventListener("message", handleMessage);
    return () => window.removeEventListener("message", handleMessage);
  }, []);

  return props;
}
