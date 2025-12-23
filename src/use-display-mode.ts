import { useOpenAIGlobal } from "./use-openai-global";
import type { DisplayMode } from "./types";

export function useDisplayMode(): DisplayMode {
  const openai = useOpenAIGlobal();
  return openai?.displayMode ?? "inline";
}
