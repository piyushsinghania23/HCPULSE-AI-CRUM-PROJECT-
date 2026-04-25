import { useEffect, useMemo, useState } from "react";

const baseState = {
  representative_name: "Field Rep",
  hcp_name: "",
  specialty: "",
  interaction_type: "Detailing",
  channel: "Field Visit",
  interaction_date: new Date().toISOString().slice(0, 10),
  notes_raw: "",
  notes_summary: "",
  products_discussed: "",
  follow_up_action: "",
  follow_up_date: ""
};

export default function LogInteractionForm({ initialData, onSubmit, isSaving }) {
  const isEditMode = Boolean(initialData?.id);
  const initialState = useMemo(() => {
    if (!initialData) return baseState;
    return {
      ...baseState,
      ...initialData,
      follow_up_date: initialData.follow_up_date || ""
    };
  }, [initialData]);

  const [formState, setFormState] = useState(initialState);

  useEffect(() => {
    setFormState(initialState);
  }, [initialState]);

  const setField = (key, value) => {
    setFormState((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const payload = {
      ...formState,
      key_entities: initialData?.key_entities || {}
    };
    onSubmit(payload);
  };

  return (
    <form className="card form-grid" onSubmit={handleSubmit}>
      <div className="card-title">{isEditMode ? "Edit Interaction" : "Structured Log Form"}</div>
      <label>
        Representative
        <input
          value={formState.representative_name}
          onChange={(e) => setField("representative_name", e.target.value)}
          required
        />
      </label>
      <label>
        HCP Name
        <input value={formState.hcp_name} onChange={(e) => setField("hcp_name", e.target.value)} required />
      </label>
      <label>
        Specialty
        <input value={formState.specialty} onChange={(e) => setField("specialty", e.target.value)} required />
      </label>
      <label>
        Interaction Type
        <select
          value={formState.interaction_type}
          onChange={(e) => setField("interaction_type", e.target.value)}
        >
          <option>Detailing</option>
          <option>Scientific Exchange</option>
          <option>Sample Drop</option>
          <option>Medical Education</option>
        </select>
      </label>
      <label>
        Channel
        <select value={formState.channel} onChange={(e) => setField("channel", e.target.value)}>
          <option>Field Visit</option>
          <option>Virtual</option>
          <option>Phone</option>
          <option>Conference</option>
        </select>
      </label>
      <label>
        Interaction Date
        <input
          type="date"
          value={formState.interaction_date}
          onChange={(e) => setField("interaction_date", e.target.value)}
          required
        />
      </label>
      <label className="full-width">
        Raw Notes
        <textarea
          rows={5}
          value={formState.notes_raw}
          onChange={(e) => setField("notes_raw", e.target.value)}
          required
          placeholder="Capture what happened in the visit..."
        />
      </label>
      <label className="full-width">
        Products Discussed
        <input
          value={formState.products_discussed}
          onChange={(e) => setField("products_discussed", e.target.value)}
          placeholder="Product A, Product B"
        />
      </label>
      <label className="full-width">
        Follow-up Action
        <input
          value={formState.follow_up_action}
          onChange={(e) => setField("follow_up_action", e.target.value)}
          placeholder="Send trial protocol summary"
        />
      </label>
      <label>
        Follow-up Date
        <input
          type="date"
          value={formState.follow_up_date}
          onChange={(e) => setField("follow_up_date", e.target.value)}
        />
      </label>
      <button className="primary-button" type="submit" disabled={isSaving}>
        {isSaving ? "Saving..." : isEditMode ? "Update Interaction" : "Log Interaction"}
      </button>
    </form>
  );
}

