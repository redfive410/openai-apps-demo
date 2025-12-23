export type DisplayMode = "inline" | "full" | "detached";

export interface WidgetProps<T = any> {
  displayMode?: DisplayMode;
  structuredContent?: T;
  maxHeight?: number;
}

export interface OpenAIGlobal {
  displayMode?: DisplayMode;
  requestMaxHeight?: (height: number) => void;
  toolOutput?: any;
  callTool?: (args: { name: string; arguments?: any }) => Promise<any>;
  setWidgetState?: (state: any) => void;
  getWidgetState?: () => any;
}

export const SET_GLOBALS_EVENT_TYPE = "openai:set_globals";
export class SetGlobalsEvent extends CustomEvent<{
  globals: Partial<OpenAIGlobal>;
}> {
  readonly type = SET_GLOBALS_EVENT_TYPE;
}

declare global {
  interface Window {
    openai?: OpenAIGlobal;
  }

  interface WindowEventMap {
    [SET_GLOBALS_EVENT_TYPE]: SetGlobalsEvent;
  }
}
