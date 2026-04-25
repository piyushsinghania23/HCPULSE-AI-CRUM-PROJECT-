export default function InteractionList({ items, onEdit }) {
  return (
    <section className="card">
      <div className="card-title">Recent Interaction Timeline</div>
      <div className="timeline">
        {items.length === 0 && <p className="muted">No records yet. Start by logging one interaction.</p>}
        {items.map((item) => (
          <article key={item.id} className="timeline-item">
            <div className="timeline-header">
              <strong>{item.hcp_name}</strong>
              <span>{item.interaction_date}</span>
            </div>
            <p className="muted">{item.specialty}</p>
            <p>{item.notes_summary || item.notes_raw}</p>
            <p className="muted">
              {item.channel} | {item.interaction_type}
            </p>
            <button className="secondary-button" onClick={() => onEdit(item)}>
              Edit Interaction
            </button>
          </article>
        ))}
      </div>
    </section>
  );
}

