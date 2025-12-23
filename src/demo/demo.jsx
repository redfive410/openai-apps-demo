import { useOpenAIGlobal } from "../use-openai-global";
import "./demo.css";

export default function App() {
  const toolOutput = useOpenAIGlobal("toolOutput");

  return (
    <div className="demo-container">
      <h1>Tool Output Display</h1>

      {!toolOutput ? (
        <div className="no-data">
          <p>No tool output available</p>
          <p className="hint">Tool output will appear here when available from window.openai.toolOutput</p>
        </div>
      ) : (
        <div className="tool-output">
          <h2>Tool Output Data:</h2>
          <pre className="output-content">
            {typeof toolOutput === "string"
              ? toolOutput
              : JSON.stringify(toolOutput, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
