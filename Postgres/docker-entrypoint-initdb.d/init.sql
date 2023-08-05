CREATE DATABASE bbcdb;

\c bbcdb

CREATE SCHEMA bbcfood;

CREATE TABLE bbcfood.recipes (
  uuid UUID PRIMARY KEY,
  href TEXT,
  title TEXT NOT NULL,
  author TEXT,
  category TEXT,
  preparation_time TEXT,
  cooking_time TEXT,
  servings TEXT,
  ingredients TEXT ARRAY,
  methods TEXT ARRAY
);

CREATE TABLE bbcfood.ingredients (
  uuid UUID NOT NULL,
  href TEXT,
  title TEXT,
  ingredient TEXT NOT NULL
);

CREATE TABLE bbcfood.methods (
  uuid UUID NOT NULL,
  href TEXT,
  title TEXT,
  step TEXT NOT NULL
);
