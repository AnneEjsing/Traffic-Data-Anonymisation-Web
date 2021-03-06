
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
    video_thumbnail text,
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
INSERT INTO public.video_settings(recording_limit,keep_days) VALUES (18000,1);


INSERT INTO users (user_id,email,role,password)
VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11','notadmin@notadmin.no', 'user', crypt('passpass', gen_salt('bf'))
) RETURNING *;

INSERT INTO users (user_id,email,role,password)
VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b12','admin@admin.no', 'admin', crypt('passpass', gen_salt('bf'))
) RETURNING *;

INSERT INTO cameras (camera_id,owner,label,description,ip,source, model_licens, model_face)
VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b12', 'open cam', 'This is a description for the open cam', '0.0.0.0','https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8', 'Default', 'Default'
) RETURNING *;

INSERT INTO cameras (camera_id,owner,label,description,ip,source, model_licens, model_face)
VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b12', 'closed cam', 'This is a very elaborate description of the camera closed to the public. Much exclusive, such rare, wow.', '0.0.0.0', 'https://bitdash-a.akamaihd.net/content/MI201109210084_1/m3u8s/f08e80da-bf1d-4e3d-8899-f0f6155f6efa.m3u8', 'Default', 'Default'
) RETURNING *;

INSERT INTO cameras (camera_id,owner,label,description,ip,source, model_licens, model_face)
VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b12', 'Best movie', 'This is not a live stream. However it is a good movie, so you should watch it', '0.0.0.0','https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8', 'Default', 'Default'
) RETURNING *;

INSERT INTO access_rights (camera_id, user_id)
VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11'
) RETURNING *;

INSERT INTO recorded_videos (video_id, video_thumbnail, camera_id, user_id, save_time)
VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380c11', 'new vid', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11', '2020-06-22 19:10:25-07'
) RETURNING *;

INSERT INTO recordings (camera_id, user_id, start_time, recording_time, recording_intervals)
VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11', '2020-06-22 19:10:25-07', '7000', '7'
) RETURNING *;