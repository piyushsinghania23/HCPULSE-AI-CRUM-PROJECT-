CREATE TABLE IF NOT EXISTS interactions (
  id SERIAL PRIMARY KEY,
  representative_name VARCHAR(120) NOT NULL,
  hcp_name VARCHAR(120) NOT NULL,
  specialty VARCHAR(120) NOT NULL,
  interaction_type VARCHAR(60) NOT NULL,
  channel VARCHAR(60) NOT NULL,
  interaction_date DATE NOT NULL,
  notes_raw TEXT NOT NULL,
  notes_summary TEXT NOT NULL,
  key_entities TEXT NOT NULL DEFAULT '{}',
  products_discussed TEXT NOT NULL DEFAULT '',
  follow_up_action TEXT NOT NULL DEFAULT '',
  follow_up_date DATE NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_interactions_hcp_name ON interactions(hcp_name);
CREATE INDEX IF NOT EXISTS idx_interactions_interaction_date ON interactions(interaction_date DESC);

