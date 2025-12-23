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

declare global {
  interface Window {
    openai?: OpenAIGlobal;
  }
}
