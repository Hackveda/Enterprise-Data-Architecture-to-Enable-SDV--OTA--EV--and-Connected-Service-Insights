-- Provision project objects inside the already-authorized Snowflake platform.
-- This script intentionally does not assume ACCOUNTADMIN and does not create
-- a new database, warehouse, or roles. Those are supplied through .env.

USE DATABASE ENTERPRISE_PLATFORM;
USE WAREHOUSE PLATFORM_WH;
USE ROLE PLATFORM_ROLE;

CREATE SCHEMA IF NOT EXISTS RAW;
CREATE SCHEMA IF NOT EXISTS STAGING;
CREATE SCHEMA IF NOT EXISTS CURATED;
CREATE SCHEMA IF NOT EXISTS MARTS;
CREATE SCHEMA IF NOT EXISTS GOVERNED;
CREATE SCHEMA IF NOT EXISTS GOVERNANCE;

-- Keep deployment idempotent and scoped to ENTERPRISE_PLATFORM.
-- Object-level grants are unnecessary here because PLATFORM_ROLE owns/creates
-- the project schemas and objects directly in this environment.
