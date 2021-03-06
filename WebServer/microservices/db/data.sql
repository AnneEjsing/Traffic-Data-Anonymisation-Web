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
    password text NOT NULL
);

CREATE TABLE public.cameras (
    camera_id uuid DEFAULT public.gen_random_uuid() NOT NULL PRIMARY KEY,
    description text,
    label text,
    ip text,
    source text UNIQUE NOT NULL,
    last_sign_of_life timestamp,
    owner uuid REFERENCES public.users(user_id) ON DELETE SET NULL,
    model_licens text,
    model_face text
);

CREATE TABLE public.video_settings (
    recording_limit integer NOT NULL, -- seconds
    keep_days integer NOT NULL -- How old a video can be, before deleted
);

CREATE TABLE public.recorded_videos (
    video_id uuid DEFAULT public.gen_random_uuid() NOT NULL PRIMARY KEY,
    user_id uuid REFERENCES public.users(user_id) ON DELETE CASCADE,
    camera_id uuid REFERENCES public.cameras(camera_id) ON DELETE SET NULL,
    save_time timestamp NOT NULL
);

CREATE TABLE public.access_rights (
    camera_id uuid NOT NULL REFERENCES public.cameras(camera_id) ON DELETE CASCADE,
    user_id uuid NOT NULL REFERENCES public.users(user_id) ON DELETE CASCADE
);

ALTER TABLE ONLY public.access_rights
    ADD CONSTRAINT access_rights_pkey PRIMARY KEY (camera_id,user_id);

CREATE TABLE public.recordings (
    camera_id uuid NOT NULL REFERENCES public.cameras(camera_id) ON DELETE CASCADE,
    user_id uuid NOT NULL REFERENCES public.users(user_id) ON DELETE CASCADE,
    start_time timestamp NOT NULL,
    recording_time integer NOT NULL,
    recording_intervals integer NOT NULL
);

ALTER TABLE ONLY public.recordings
    ADD CONSTRAINT recordings_pkey PRIMARY KEY (camera_id,user_id);

-- Table ownership
ALTER TABLE public.users OWNER TO postgres;
ALTER TABLE public.recorded_videos OWNER TO postgres;
ALTER TABLE public.cameras OWNER TO postgres;
ALTER TABLE public.access_rights OWNER TO postgres;
ALTER TABLE public.video_settings OWNER TO postgres;
ALTER TABLE public.recordings OWNER TO postgres;

-- Start up data
INSERT INTO public.video_settings(recording_limit, keep_days) VALUES (18000, 1);
