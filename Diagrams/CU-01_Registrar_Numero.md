# Caso de Uso: Registrar Numero de Loteria

## Identificador
CU-01

## Objetivo
Permitir al administrador registrar un numero de loteria vendido a un cliente para que participe en un sorteo.

## Actores
- Actor Principal: Administrador
- Actores Secundarios: Ninguno

## Disparador
El administrador selecciona la opcion "Registrar numero".

## Precondiciones
- Ninguna

## Flujo Principal
1. El administrador selecciona "Registrar numero".
2. El sistema muestra el formulario de registro.
3. El administrador ingresa el numero (4 cifras), el nombre del propietario y la fecha del sorteo.
4. El sistema valida que el numero tenga exactamente 4 cifras.
5. El sistema valida que la fecha del sorteo no haya pasado.
6. El sistema verifica que el numero no este registrado para esa misma fecha.
7. El sistema almacena el registro con estado "Activo".
8. El sistema muestra mensaje de confirmacion "Numero registrado exitosamente".

## Flujos Alternativos

| ID    | Descripcion |
|-------|-------------|
| FA-01 | El administrador cancela la operacion. El sistema descarta los datos y regresa al menu principal. |

## Flujos de Excepcion

| ID    | Descripcion |
|-------|-------------|
| FE-01 | El numero no tiene exactamente 4 cifras. El sistema muestra error de validacion. |
| FE-02 | La fecha del sorteo ya paso. El sistema muestra error "No se permite registrar numeros para sorteos cuya fecha ya paso". |
| FE-03 | El numero ya existe para la misma fecha de sorteo. El sistema muestra error "Numero duplicado". |

## Postcondiciones
- El numero queda almacenado en el sistema con estado "Activo".

## Reglas de Negocio
- RN-01: Todo numero debe ser de exactamente 4 cifras (0000-9999).
- RN-02: No se pueden registrar numeros para sorteos cuya fecha ya paso.
- RN-03: Un mismo numero no se puede vender dos veces para el mismo sorteo.

## Prioridad
Alta

## Frecuencia de Uso
Alta

## Casos Relacionados
- CU-04: Listar numeros de loteria
