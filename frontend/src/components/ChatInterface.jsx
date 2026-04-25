import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { pushUserMessage, sendChatMessage } from "../store/chatSlice";

export default function ChatInterface() {
  const dispatch = useDispatch();
  const [message, setMessage] = useState("");
  const [hcpName, setHcpName] = useState("");
  const [repName, setRepName] = useState("Field Rep");
  const { messages, status } = useSelector((state) => state.chat);

  const handleSend = async (event) => {
    event.preventDefault();
    if (!message.trim()) return;

    dispatch(
      pushUserMessage({
        id: crypto.randomUUID(),
        role: "user",
        content: message
      })
    );

    await dispatch(
      sendChatMessage({
        message,
        hcp_name: hcpName || undefined,
        representative_name: repName || undefined
      })
    );
    setMessage("");
  };

  return (
    <section className="card chat-shell">
      <div className="card-title">Conversational Copilot</div>
      <div className="chat-metadata">
        <input value={repName} onChange={(e) => setRepName(e.target.value)} placeholder="Representative name" />
        <input value={hcpName} onChange={(e) => setHcpName(e.target.value)} placeholder="HCP context (optional)" />
      </div>
      <div className="chat-feed">
        {messages.map((msg) => (
          <div key={msg.id} className={`bubble ${msg.role}`}>
            <p>{msg.content}</p>
          </div>
        ))}
      </div>
      <form className="chat-input" onSubmit={handleSend}>
        <input
          placeholder="Try: Log today’s visit with Dr. Shah and capture key objections..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <button className="primary-button" type="submit" disabled={status === "loading"}>
          {status === "loading" ? "Thinking..." : "Send"}
        </button>
      </form>
    </section>
  );
}

