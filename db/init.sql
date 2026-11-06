CREATE TABLE accounts (
    id           TEXT PRIMARY KEY,
    owner        TEXT NOT NULL,
    balance_kobo BIGINT NOT NULL CHECK (balance_kobo >= 0)
);
CREATE TABLE transfers (
    id           UUID PRIMARY KEY,
    from_account TEXT NOT NULL,
    to_account   TEXT NOT NULL,
    amount_kobo  BIGINT NOT NULL CHECK (amount_kobo > 0),
    narration    TEXT DEFAULT '',
    status       TEXT NOT NULL,
    reason       TEXT,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX transfers_created_at_idx ON transfers (created_at DESC);
INSERT INTO accounts VALUES
  ('ACC001', 'Adaeze Stores',      50000000),
  ('ACC002', 'Tunde Logistics',    25000000),
  ('ACC003', 'Ngozi Pharmacy',     10000000),
  ('ACC004', 'Musa Agro Supplies', 75000000);
