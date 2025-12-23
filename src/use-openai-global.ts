import { useEffect, useState } from "react";
import type { OpenAIGlobal } from "./types";

export function useOpenAIGlobal(): OpenAIGlobal | null {
  const [openai, setOpenai] = useState<OpenAIGlobal | null>(
    typeof window !== "undefined" ? window.openai ?? null : null
  );

  useEffect(() => {
    if (typeof window === "undefined") return;

    const check = () => {
      if (window.openai && window.openai !== openai) {
        setOpenai(window.openai);
      }
    };

    const interval = setInterval(check, 100);
    return () => clearInterval(interval);
  }, [openai]);

  return openai;
}
