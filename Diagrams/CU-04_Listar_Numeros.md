# Caso de Uso: Listar Numeros de Loteria

## Identificador
CU-04

## Objetivo
Permitir al administrador consultar los numeros registrados para un sorteo en particular.

## Actores
- Actor Principal: Administrador
- Actores Secundarios: Ninguno

## Disparador
El administrador selecciona "Listar numeros".

## Precondiciones
- Ninguna

## Flujo Principal
1. El administrador selecciona "Listar numeros".
2. El sistema muestra todos los numeros registrados con: Numero, Propietario, Fecha del sorteo.

## Flujos Alternativos

| ID    | Descripcion |
|-------|-------------|
| FA-01 | El administrador filtra por fecha de sorteo. El sistema muestra solo los numeros de esa fecha. |

## Flujos de Excepcion

| ID    | Descripcion |
|-------|-------------|
| FE-01 | No existen registros. El sistema muestra mensaje "No hay numeros registrados". |

## Postcondiciones
- El sistema presenta la informacion solicitada al administrador.

## Reglas de Negocio
- RN-01: Mostrar numero, propietario y fecha del sorteo.

## Prioridad
Alta

## Frecuencia de Uso
Alta

## Casos Relacionados
- CU-02: Actualizar numero de loteria
- CU-03: Eliminar numero de loteria
