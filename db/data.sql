-- Initial Data for SSH Server Users
-- Passwords must be pre-hashed in SHA-256
INSERT INTO users (username, password_hash) VALUES ('admin', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f'); -- password: password123
INSERT INTO users (username, password_hash) VALUES ('alice', 'b92d6e32bc00ee2ebef7e3e9d8995a9ffc039752c0021b16cdbf940d9904c632'); -- password: linux-forever
INSERT INTO users (username, password_hash) VALUES ('bob', '5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5'); -- password: 12345