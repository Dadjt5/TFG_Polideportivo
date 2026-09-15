# TFG_Polideportivo

Aplicación web full-stack para la gestión de un polideportivo, desarrollada como **Trabajo de Fin de Grado (TFG)**.

El proyecto está compuesto por un frontend desarrollado con **Vue.js** y un backend desarrollado con **Django + Django REST Framework**, comunicados mediante una **API REST**.

## Demo

**Aplicación en producción:** https://polideportivo-xg7l.onrender.com/home

## Tecnologías

**Frontend**

* Vue.js
* JavaScript
* HTML / CSS

**Backend**

* Python
* Django
* Django REST Framework
* JWT Authentication

**Base de datos**

* PostgreSQL
* Neon

**Deployment**

* Render

## Funcionalidades

* Gestión de usuarios y autenticación mediante JWT
* Gestión de instalaciones deportivas
* Gestión y consulta de reservas
* Gestión de información del polideportivo
* Comunicación entre frontend y backend mediante API REST
* Persistencia de datos mediante PostgreSQL
* Despliegue de la aplicación en producción

## Arquitectura

```text
┌──────────────────┐
│   Vue.js         │
│    Frontend      │
└────────┬─────────┘
         │
      REST API
         │
┌────────▼─────────┐
│ Django + DRF     │
│     Backend      │
└────────┬─────────┘
         │
┌────────▼─────────┐
│   PostgreSQL     │
│      Neon        │
└──────────────────┘
```

## Estructura del proyecto

```text
TFG_Polideportivo/
├── frontend/
├── backend/
└── README.md
```

## Sobre el proyecto

Este proyecto fue desarrollado como mi **Trabajo de Fin de Grado**, aplicando conocimientos de desarrollo web full-stack, diseño de APIs REST, gestión de bases de datos, autenticación y despliegue de aplicaciones.

El objetivo principal fue desarrollar una plataforma web que centralizara la gestión de las diferentes funcionalidades de un polideportivo.

## Autor

Desarrollado por **David Juzgado Torell**.
