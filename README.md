# Implementación loteria

## Jorge Humberto Gaviria Botero

link pagina: https://jorgegaviria.pythonanywhere.com/

### Modelo verbal

Una empresa de lotería organiza sorteos semanales. En cada sorteo se define un número ganador de 4 cifras (del 0000 al 9999). Los clientes compran boletas que contienen un número de 4 cifras, el cual participa en el sorteo de una fecha determinada.

El sistema administra los números vendidos. Cada número tiene un propietario (la persona que lo compró) y pertenece a un sorteo específico (identificado por su fecha).

Las restricciones son las siguientes:

Todo número debe ser de exactamente 4 cifras.
Un mismo número no se puede vender dos veces para el mismo sorteo.
No se pueden registrar números para sorteos cuya fecha ya pasó.
Solo se pueden modificar o eliminar números cuya fecha de sorteo aún no ha pasado.
El administrador es el único usuario del sistema. Él se encarga de registrar los números vendidos, corregir datos si hubo un error, eliminar una venta si el cliente la cancela, y consultar los números registrados para un sorteo en particular.
