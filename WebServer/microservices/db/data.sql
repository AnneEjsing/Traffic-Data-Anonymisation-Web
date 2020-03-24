-- Initial settings

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

\connect "traffic_annonymisation_db"

-- Access type
CREATE TYPE rights AS ENUM ('user', 'admin');

-- For uuid's
CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;

-- Actual tables
CREATE TABLE public.users (
    user_id uuid DEFAULT public.gen_random_uuid() NOT NULL PRIMARY KEY,
    email text UNIQUE NOT NULL,
    role rights NOT NULL,
    password text NOT NULL,
    salt text NOT NULL
);

CREATE TABLE public.cameras (
    camera_id uuid DEFAULT public.gen_random_uuid() NOT NULL PRIMARY KEY,
    description text,
    ip text,
    last_sign_of_life timestamp NOT NULL,
    owner uuid NOT NULL REFERENCES public.users(user_id)
);

CREATE TABLE public.recorded_videos (
    videoid uuid DEFAULT public.gen_random_uuid() NOT NULL PRIMARY KEY,
    user_id uuid NOT NULL REFERENCES public.users(user_id),
    camera_id uuid NOT NULL REFERENCES public.cameras(camera_id),
    video_file text NOT NULL,
    video_thumbnail text,
    save_time timestamp NOT NULL
);

CREATE TABLE public.access_rights (
    camera_id uuid NOT NULL REFERENCES public.cameras(camera_id) ON DELETE CASCADE,
    user_id uuid NOT NULL REFERENCES public.users(user_id) ON DELETE CASCADE,
    expiry timestamp
);

ALTER TABLE ONLY public.access_rights
    ADD CONSTRAINT access_rights_pkey PRIMARY KEY (camera_id,user_id);


-- Table ownership
ALTER TABLE public.users OWNER TO postgres;
ALTER TABLE public.recorded_videos OWNER TO postgres;
ALTER TABLE public.cameras OWNER TO postgres;
ALTER TABLE public.access_rights OWNER TO postgres;
