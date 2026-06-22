# Caso de Uso: Eliminar Numero de Loteria

## Identificador
CU-03

## Objetivo
Permitir al administrador eliminar un numero de loteria si el cliente cancela su compra.

## Actores
- Actor Principal: Administrador
- Actores Secundarios: Ninguno

## Disparador
El administrador selecciona un numero del listado y elige "Eliminar".

## Precondiciones
- Existe al menos un numero registrado.

## Flujo Principal
1. El sistema muestra el listado de numeros (CU-04).
2. El administrador selecciona el numero a eliminar.
3. El sistema muestra los datos del registro.
4. El sistema solicita confirmacion de eliminacion.
5. El administrador confirma la eliminacion.
6. El sistema valida que el sorteo no se haya realizado.
7. El sistema elimina el registro.
8. El sistema muestra mensaje de confirmacion.

## Flujos Alternativos

| ID    | Descripcion |
|-------|-------------|
| FA-01 | El administrador cancela la operacion. El sistema no elimina y regresa al listado. |

## Flujos de Excepcion

| ID    | Descripcion |
|-------|-------------|
| FE-01 | El sorteo ya se realizo. El sistema no permite la eliminacion. |

## Postcondiciones
- El registro queda eliminado del sistema.
- El numero ya no aparece en el listado.

## Reglas de Negocio
- RN-01: Solo se pueden eliminar numeros de sorteos que aun no se han realizado.

## Prioridad
Media

## Frecuencia de Uso
Baja

## Casos Relacionados
- CU-01: Registrar numero de loteria
- CU-04: Listar numeros de loteria
