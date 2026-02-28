-- Initial Data for SSH Server Users
-- Passwords must be pre-hashed in SHA-256
INSERT INTO users (username, password_hash) VALUES ('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9'); -- password: admin123
INSERT INTO users (username, password_hash) VALUES ('alice', 'c72350ddcfc2a5e0080cedc54c02970e3db67a9ca39d4d5c86408a977a9ec682'); -- password: ecila
INSERT INTO users (username, password_hash) VALUES ('bob', 'f3029a66c61b61b41b428963a2fc134154a5383096c776f3b4064733c5463d90'); -- password: azerty123
INSERT INTO users (username, password_hash) VALUES ('ayoub', '8347c141afce47f4ebb66e097af7ae3e7ff7d703d37044071ad94228c28d2017'); -- password: ------