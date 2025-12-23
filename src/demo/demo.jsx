import { useOpenAIGlobal } from "../use-openai-global";
import { Markdown } from "@openai/apps-sdk-ui/components/Markdown";
import "./demo.css";

export default function App() {
  const toolOutput = useOpenAIGlobal("toolOutput");

  const jsonOutput = !toolOutput
    ? null
    : typeof toolOutput === "string"
    ? toolOutput
    : JSON.stringify(toolOutput, null, 2);

  const markdownContent = jsonOutput
    ? `\`\`\`json\n${jsonOutput}\n\`\`\``
    : null;

  return (
    <div className="demo-container">
      <h1>Tool Output Display</h1>

      {!markdownContent ? (
        <div className="no-data">
          <p>No tool output available</p>
          <p className="hint">Tool output will appear here when available from window.openai.toolOutput</p>
        </div>
      ) : (
        <div className="tool-output">
          <h2>Tool Output Data:</h2>
          <Markdown>{markdownContent}</Markdown>
        </div>
      )}
    </div>
  );
}
