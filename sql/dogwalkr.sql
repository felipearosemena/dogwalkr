

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

SET default_tablespace = '';

SET default_with_oids = false;


CREATE TABLE "public"."alembic_version" (
    "version_num" character varying(32) NOT NULL
);



CREATE TABLE "public"."dogs" (
    "id" integer NOT NULL,
    "name" character varying(255),
    "owner_id" integer NOT NULL,
    "created_at" timestamp without time zone,
    "updated_at" timestamp without time zone
);



CREATE SEQUENCE "public"."dogs_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



ALTER SEQUENCE "public"."dogs_id_seq" OWNED BY "public"."dogs"."id";



CREATE TABLE "public"."users" (
    "id" integer NOT NULL,
    "name" character varying(255),
    "created_at" timestamp without time zone,
    "updated_at" timestamp without time zone
);



CREATE SEQUENCE "public"."users_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



ALTER SEQUENCE "public"."users_id_seq" OWNED BY "public"."users"."id";



ALTER TABLE ONLY "public"."dogs" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."dogs_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."users" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."users_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."alembic_version"
    ADD CONSTRAINT "alembic_version_pkc" PRIMARY KEY ("version_num");



ALTER TABLE ONLY "public"."dogs"
    ADD CONSTRAINT "dogs_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."users"
    ADD CONSTRAINT "users_pkey" PRIMARY KEY ("id");



CREATE INDEX "ix_dogs_id" ON "public"."dogs" USING "btree" ("id");



CREATE INDEX "ix_users_id" ON "public"."users" USING "btree" ("id");



ALTER TABLE ONLY "public"."dogs"
    ADD CONSTRAINT "dogs_owner_id_fkey" FOREIGN KEY ("owner_id") REFERENCES "public"."users"("id");


CREATE TABLE "public"."toys" (
    "id" integer NOT NULL,
    "name" character varying(255),
    "dog_owner_id" integer NOT NULL,
    "created_at" timestamp without time zone,
    "updated_at" timestamp without time zone
);



CREATE SEQUENCE "public"."toys_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE "public"."toys_id_seq" OWNED BY "public"."toys"."id";


ALTER TABLE ONLY "public"."toys" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."toys_id_seq"'::"regclass");

ALTER TABLE ONLY "public"."toys"
    ADD CONSTRAINT "toys_pkey" PRIMARY KEY ("id");

CREATE INDEX "ix_toys_id" ON "public"."toys" USING "btree" ("id");

ALTER TABLE ONLY "public"."toys"
    ADD CONSTRAINT "toys_dog_owner_id_fkey" FOREIGN KEY ("dog_owner_id") REFERENCES "public"."dogs"("id");



