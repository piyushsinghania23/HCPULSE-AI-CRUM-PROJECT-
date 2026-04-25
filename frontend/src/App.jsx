import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import ChatInterface from "./components/ChatInterface";
import InteractionList from "./components/InteractionList";
import LogInteractionForm from "./components/LogInteractionForm";
import { createInteraction, fetchInteractions, updateInteraction } from "./store/interactionsSlice";

export default function App() {
  const dispatch = useDispatch();
  const { items, status } = useSelector((state) => state.interactions);
  const [mode, setMode] = useState("form");
  const [editTarget, setEditTarget] = useState(null);

  useEffect(() => {
    dispatch(fetchInteractions());
  }, [dispatch]);

  const onSubmitForm = async (payload) => {
    if (editTarget?.id) {
      await dispatch(updateInteraction({ id: editTarget.id, payload }));
      setEditTarget(null);
      return;
    }
    await dispatch(createInteraction(payload));
  };

  return (
    <main className="layout">
      <header className="hero">
        <p className="eyebrow">AI-First CRM | HCP Module</p>
        <h1>Log Interaction Screen</h1>
        <p>
          Field reps can capture HCP interactions through a structured form or a LangGraph chat copilot.
        </p>
      </header>

      <div className="mode-toggle">
        <button
          className={mode === "form" ? "active-tab" : ""}
          onClick={() => setMode("form")}
        >
          Structured Form
        </button>
        <button
          className={mode === "chat" ? "active-tab" : ""}
          onClick={() => setMode("chat")}
        >
          Conversational Chat
        </button>
      </div>

      <section className="grid-2">
        {mode === "form" ? (
          <LogInteractionForm
            initialData={editTarget}
            isSaving={status === "loading"}
            onSubmit={onSubmitForm}
          />
        ) : (
          <ChatInterface />
        )}
        <InteractionList items={items} onEdit={(item) => setEditTarget(item)} />
      </section>
    </main>
  );
}

