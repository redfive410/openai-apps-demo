import { useState, useEffect } from "react";
import { useOpenAIGlobal } from "../use-openai-global";
import { Markdown } from "@openai/apps-sdk-ui/components/Markdown";
import { Button, ButtonLink } from "@openai/apps-sdk-ui/components/Button";
import { EmptyMessage } from "@openai/apps-sdk-ui/components/EmptyMessage";
import "./demo.css";

export default function App() {
  const initialToolOutput = useOpenAIGlobal("toolOutput");
  const initialToolResponseMetadata = useOpenAIGlobal("toolResponseMetadata");

  // Use local state to manage the current tool output
  const [toolOutput, setToolOutput] = useState(initialToolOutput);
  const [toolResponseMetadata, setToolResponseMetadata] = useState(initialToolResponseMetadata);

  // Update local state when initial values change
  useEffect(() => {
    setToolOutput(initialToolOutput);
  }, [initialToolOutput]);

  useEffect(() => {
    setToolResponseMetadata(initialToolResponseMetadata);
  }, [initialToolResponseMetadata]);

  const jsonOutput = !toolOutput
    ? null
    : typeof toolOutput === "string"
    ? toolOutput
    : JSON.stringify(toolOutput, null, 2);

  const markdownContent = jsonOutput
    ? `\`\`\`json\n${jsonOutput}\n\`\`\``
    : null;

  const handleResetTool = async () => {
    if (window.openai?.callTool) {
      try {
        const result = await window.openai.callTool("reset", {});
        // Update local state with the new tool output
        if (result?.structuredContent) {
          setToolOutput(result.structuredContent);
        }
        if (result?._meta) {
          setToolResponseMetadata(result._meta);
        }
      } catch (error) {
        console.error("Error calling reset tool:", error);
      }
    } else {
      console.error("window.openai.callTool is not available");
    }
  };

  return (
    <div className="demo-container">
      <h1>ChatGPT Apps Demo</h1>

      {!markdownContent ? (
        <EmptyMessage>
          No tool output available. Tool output will appear here when available from window.openai.toolOutput.
        </EmptyMessage>
      ) : (
        <div className="tool-output">
          <h2>Tool Output Data:</h2>
          <Markdown>{markdownContent}</Markdown>
          {toolOutput && (
            <div>
              <h2>Tool Output Message:</h2>
              {toolOutput.message && (
                <p style={{ padding: '10px', background: '#f0f0f0', borderRadius: '5px' }}>
                  <strong>message:</strong> {toolOutput.message}
                </p>
              )}
              <h2>Tool Response Metadata:</h2>
              {toolResponseMetadata?.["demo/myKey"] && (
                <p style={{ padding: '10px', background: '#e8f4f8', borderRadius: '5px' }}>
                  <strong>demo/myKey:</strong> {toolResponseMetadata["demo/myKey"]}
                </p>
              )}
            </div>
          )}
        </div>
      )}

      <div style={{ marginTop: '20px', display: 'flex', gap: '10px' }}>
        <Button
          color="danger"
          onClick={handleResetTool}
        >
          Reset
        </Button>
        <ButtonLink
          color="primary"
          href="https://www.tramalfadore.com"
        >
          Visit Tramalfadore
        </ButtonLink>
      </div>
    </div>
  );
}
