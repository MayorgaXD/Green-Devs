# GreenDevs: Eco-Mercado Digital Orientado a la Mitigación de Pérdidas Agrícolas

## Descripción General
GreenDevs es una plataforma web e inventario digital en tiempo real diseñada para solucionar la problemática del desperdicio y la pérdida de productos agrícolas que sufren los pequeños y grandes productores en el municipio de Nueva Guinea. A través de la eliminación de intermediarios innecesarios y la optimización basada en marketing digital, el sistema facilita la conexión directa entre los agroproductores locales y las cadenas de distribución comercial o consumidores finales. 

El proyecto cuenta con un enfoque en la identidad local y el comercio justo, proveyendo herramientas tecnológicas accesibles de manera responsiva desde dispositivos móviles y de escritorio.

---

## Arquitectura y Tecnologías Utilizadas
La solución implementa una arquitectura desacoplada estructurada de la siguiente manera:

* **Backend:** Python 3.13 y Django 6.0. Se encarga del procesamiento lógico, la gestión de la base de datos relacional (SQLite en entorno de desarrollo) y la exposición de servicios mediante una API en formato JSON.
* **Frontend:** JavaScript (Fetch API) y maquetación responsiva con Tailwind CSS. Consume los servicios del servidor central para renderizar la información dinámicamente sin recargas asíncronas forzadas.
* **Seguridad y Control:** Arquitectura basada en Roles (RBAC) para el cumplimiento estricto de permisos funcionales en la plataforma.

---

## Estructura de Seguridad y Roles de Usuario
En cumplimiento con los requerimientos técnicos de la rúbrica de evaluación, el sistema integra tres perfiles de acceso claramente definidos en el modelo de datos:

1. **Administrador del Sistema (Admin):** Control total sobre la infraestructura del software, gestión de usuarios, auditoría global y mantenimiento de registros.
2. **Usuario (Productor o Comprador):** Perfil destinado a los agricultores para la publicación de su inventario real, precio sugerido, unidad de medida y descripción del estado de la cosecha. Asimismo, permite al comerciante visualizar la disponibilidad en tierra.
3. **Auditor de Calidad y Precios Justos:** Rol especializado encargado de monitorear y regular que las ofertas cargadas en la plataforma cumplan con los estándares justos del mercado, evitando la especulación y protegiendo al productor independiente.

---

## Requisitos del Sistema y Instalación Básica

### Requisitos
* Python 3.13 o superior instalado en el sistema operativo.
* Administrador de paquetes `pip` actualizado.

### Pasos para la Ejecución De Forma Local

1. **Clonar el repositorio y acceder al directorio del backend:**
   ```bash
   cd greendevs-project/BACKEND