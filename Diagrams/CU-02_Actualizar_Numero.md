# Caso de Uso: Actualizar Numero de Loteria

## Identificador
CU-02

## Objetivo
Permitir al administrador corregir los datos de un numero de loteria si hubo un error en el registro.

## Actores
- Actor Principal: Administrador
- Actores Secundarios: Ninguno

## Disparador
El administrador selecciona un numero del listado y elige "Actualizar".

## Precondiciones
- Existe al menos un numero registrado.

## Flujo Principal
1. El sistema muestra el listado de numeros (CU-04).
2. El administrador selecciona el numero a actualizar.
3. El sistema muestra los datos actuales del registro.
4. El administrador modifica el propietario y/o la fecha.
5. El sistema valida que el sorteo no se haya realizado.
6. El sistema verifica que no se genere un duplicado.
7. El sistema actualiza el registro.
8. El sistema muestra mensaje de confirmacion.

## Flujos Alternativos

| ID    | Descripcion |
|-------|-------------|
| FA-01 | El administrador cancela la operacion. El sistema descarta los cambios y regresa al listado. |

## Flujos de Excepcion

| ID    | Descripcion |
|-------|-------------|
| FE-01 | El sorteo ya se realizo. El sistema no permite la modificacion. |
| FE-02 | La modificacion genera un numero duplicado para la nueva fecha. El sistema muestra error. |

## Postcondiciones
- El registro queda actualizado con los nuevos datos.

## Reglas de Negocio
- RN-01: Solo se pueden modificar numeros de sorteos que aun no se han realizado.
- RN-02: Un mismo numero no se puede vender dos veces para el mismo sorteo.

## Prioridad
Media

## Frecuencia de Uso
Media

## Casos Relacionados
- CU-01: Registrar numero de loteria
- CU-04: Listar numeros de loteria
