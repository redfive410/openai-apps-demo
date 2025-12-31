import { useOpenAIGlobal } from "../use-openai-global";
import { Markdown } from "@openai/apps-sdk-ui/components/Markdown";
import { ButtonLink } from "@openai/apps-sdk-ui/components/Button";
import "./demo.css";

export default function App() {
  const toolOutput = useOpenAIGlobal("toolOutput");
  const toolResponseMetadata = useOpenAIGlobal("toolResponseMetadata");

  const jsonOutput = !toolOutput
    ? null
    : typeof toolOutput === "string"
    ? toolOutput
    : JSON.stringify(toolOutput, null, 2);

  const markdownContent = jsonOutput
    ? `\`\`\`json\n${jsonOutput}\n\`\`\``
    : null;

  const handleResetTool = () => {
    if (window.openai?.callTool) {
      window.openai.callTool("reset", {});
    } else {
      console.error("window.openai.callTool is not available");
    }
  };

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
            {toolResponseMetadata && (
              <div>
                <h2>Custom Metadata:</h2>
                {toolResponseMetadata.customMessage && (
                  <p style={{ padding: '10px', background: '#f0f0f0', borderRadius: '5px' }}>
                    <strong>Message:</strong> {toolResponseMetadata.customMessage}
                  </p>
                )}
                {toolResponseMetadata.timestamp && (
                  <p style={{ padding: '10px', background: '#e8f4f8', borderRadius: '5px' }}>
                    <strong>Timestamp:</strong> {toolResponseMetadata.timestamp}
                  </p>
                )}
              </div>
            )}
          </div>
          )}

      <div style={{ marginTop: '20px', display: 'flex', gap: '10px' }}>
        <button
          onClick={handleResetTool}
          style={{
            padding: '10px 20px',
            background: '#cc3300',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            fontSize: '14px',
            fontWeight: 'bold'
          }}
          onMouseOver={(e) => e.target.style.background = '#a32900'}
          onMouseOut={(e) => e.target.style.background = '#cc3300'}
        >
          Reset Counter (Tool Call Demo)
        </button>
        <ButtonLink
          color="primary"
          href="https://www.tramalfadore.com">
          Visit Tramalfadore
        </ButtonLink>
      </div>
    </div>
  );
}
