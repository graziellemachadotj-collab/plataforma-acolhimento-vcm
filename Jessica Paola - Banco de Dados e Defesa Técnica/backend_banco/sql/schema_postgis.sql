-- =====================================================================
-- Plataforma de Acolhimento, Orientação e Resposta Rápida
-- Schema PostgreSQL + PostGIS (referência)  ·  Jessica Paola Miranda Vitorino
--
-- O Python (database.py) cria tudo isto automaticamente. Este arquivo serve
-- para estudo e para quem quiser criar o banco direto no psql.
-- =====================================================================

CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE service_types (
  codigo     varchar(30) PRIMARY KEY,          -- DEAM, DEFENSORIA, CRAM, CREAS, ...
  nome       varchar(120) NOT NULL,
  descricao  text NOT NULL DEFAULT ''
);

CREATE TABLE services (
  id            serial PRIMARY KEY,
  nome          varchar(200) NOT NULL,
  service_type  varchar(30) NOT NULL REFERENCES service_types(codigo),
  telefone      varchar(40),
  site          varchar(300),
  endereco      varchar(300),                  -- endereço do SERVIÇO, nunca da usuária
  cidade        varchar(120) NOT NULL DEFAULT '',
  uf            char(2) NOT NULL DEFAULT '',
  latitude      double precision NOT NULL,
  longitude     double precision NOT NULL,
  funciona_24h  boolean NOT NULL DEFAULT false,
  exemplo       boolean NOT NULL DEFAULT false,
  verificado_em timestamptz,                   -- revisar a cada 3 a 6 meses
  location      geography(Point, 4326)
                GENERATED ALWAYS AS (ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)::geography) STORED
);
CREATE INDEX services_location_gix ON services USING GIST (location);
CREATE INDEX services_type_ix ON services (service_type);

CREATE TABLE support_contacts (
  numero varchar(10) PRIMARY KEY, nome varchar(120) NOT NULL, descricao text NOT NULL, ordem int NOT NULL DEFAULT 0
);

CREATE TABLE users (
  id            varchar(32) PRIMARY KEY,       -- ID pseudônimo
  apelido       varchar(40) UNIQUE NOT NULL,
  senha_hash    varchar(200) NOT NULL,         -- credencial derivada (scrypt)
  consentimento boolean NOT NULL DEFAULT false,
  criado_em     timestamptz NOT NULL DEFAULT now(),
  atualizado_em timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE sessions (
  token_hash varchar(64) PRIMARY KEY,          -- só o hash do token
  user_id    varchar(32) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  expira_em  timestamptz NOT NULL
);

CREATE TABLE trusted_contacts (
  id              varchar(32) PRIMARY KEY,
  user_id         varchar(32) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  nome            varchar(80) NOT NULL,
  canal           varchar(20) NOT NULL,
  contato_cifrado bytea NOT NULL,              -- cifrado (Fernet); a chave fica fora do banco
  consentimento   boolean NOT NULL DEFAULT false,
  criado_em       timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE evidence_entries (
  id               varchar(32) PRIMARY KEY,
  user_id          varchar(32) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  relato_cifrado   bytea NOT NULL,
  hash_integridade varchar(64) NOT NULL,       -- SHA-256 do relato original
  tipo_violencia   varchar(30),
  ocorrido_em      timestamptz,
  criado_em        timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE emergency_alerts (
  id                   varchar(32) PRIMARY KEY,
  user_id              varchar(32) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  latitude_aprox       double precision,       -- arredondada (~1 km)
  longitude_aprox      double precision,
  mensagem             text NOT NULL,
  contatos_notificados int NOT NULL DEFAULT 0,
  criado_em            timestamptz NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------
-- Consulta do README: DEAM em até 20 km, da mais próxima para a mais longe
-- ---------------------------------------------------------------------
-- SELECT id, nome, telefone, site,
--        ST_Distance(location, ST_SetSRID(ST_MakePoint(:longitude, :latitude), 4326)::geography) AS distance_m
--   FROM services
--  WHERE service_type = 'DEAM'
--    AND ST_DWithin(location, ST_SetSRID(ST_MakePoint(:longitude, :latitude), 4326)::geography, 20000)
--  ORDER BY distance_m
--  LIMIT 10;
