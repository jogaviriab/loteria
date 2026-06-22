"""
Catalogo de Casos de Prueba

CU-01: Registrar Numero de Loteria
| ID      | Caso de uso | Descripcion                                      | Tipo     |
|---------|-------------|--------------------------------------------------|----------|
| CP-001  | CU-01       | Registro exitoso con datos validos               | Positivo |
| CP-002  | CU-01       | Numero con valor minimo (0000)                   | Borde    |
| CP-003  | CU-01       | Numero con valor maximo (9999)                   | Borde    |
| CP-004  | CU-01       | Numero mayor a 9999 rechazado                    | Negativo |
| CP-005  | CU-01       | Numero negativo rechazado                        | Negativo |
| CP-006  | CU-01       | Numero duplicado para la misma fecha rechazado   | Negativo |
| CP-007  | CU-01       | Mismo numero en fecha diferente permitido        | Positivo |
| CP-008  | CU-01       | Campos obligatorios vacios rechazados            | Negativo |
| CP-008b | CU-01       | Fecha de sorteo pasada rechazada (FE-02)         | Negativo |
| CP-009  | CU-01       | Vista GET muestra formulario vacio               | Positivo |
| CP-010  | CU-01       | Vista POST valido redirige y muestra mensaje     | Positivo |
| CP-011  | CU-01       | Vista POST invalido muestra errores en form      | Negativo |
| CP-011b | CU-01       | Vista POST fecha pasada rechazado (FE-02)        | Negativo |
| CP-012  | CU-01       | Vista POST duplicado muestra error de duplicado  | Negativo |

CU-02: Actualizar Numero de Loteria
| ID     | Caso de uso | Descripcion                                              | Tipo     |
|--------|-------------|----------------------------------------------------------|----------|
| CP-013 | CU-02       | Actualizacion exitosa con datos validos                  | Positivo |
| CP-014 | CU-02       | Vista GET muestra formulario con datos actuales          | Positivo |
| CP-015 | CU-02       | Fecha de sorteo ya paso, redirige con error (FE-01)      | Negativo |
| CP-016 | CU-02       | Numero duplicado para nueva fecha rechazado (FE-03)      | Negativo |
| CP-017 | CU-02       | Numero invalido (>9999) rechazado (FE-02)                | Negativo |
| CP-018 | CU-02       | Cambiar fecha a pasada en formulario rechazado           | Negativo |
| CP-019 | CU-02       | Actualizar propietario sin cambiar numero ni fecha       | Positivo |
| CP-020 | CU-02       | Registro inexistente retorna 404                         | Negativo |

CU-03: Eliminar Numero de Loteria
| ID     | Caso de uso | Descripcion                                              | Tipo     |
|--------|-------------|----------------------------------------------------------|----------|
| CP-021 | CU-03       | Eliminacion exitosa con confirmacion                     | Positivo |
| CP-022 | CU-03       | Vista GET muestra datos y solicita confirmacion           | Positivo |
| CP-023 | CU-03       | Fecha de sorteo ya paso, redirige con error (FE-01)      | Negativo |
| CP-024 | CU-03       | Cancelar eliminacion regresa al listado (FA-01)          | Positivo |
| CP-025 | CU-03       | Registro inexistente retorna 404                         | Negativo |
| CP-026 | CU-03       | Registro eliminado ya no aparece en listado              | Positivo |

CU-04: Listar Numeros de Loteria
| ID     | Caso de uso | Descripcion                                              | Tipo     |
|--------|-------------|----------------------------------------------------------|----------|
| CP-027 | CU-04       | Listar todos los numeros registrados                     | Positivo |
| CP-028 | CU-04       | Listar sin registros muestra mensaje vacio (FE-01)       | Negativo |
| CP-029 | CU-04       | Filtrar por fecha muestra solo esa fecha (FA-01)         | Positivo |
| CP-030 | CU-04       | Filtrar por fecha sin resultados muestra mensaje vacio   | Negativo |
| CP-031 | CU-04       | Listado muestra todos los campos requeridos (RN-01)      | Positivo |
"""

from datetime import date, timedelta
from django.test import TestCase, Client
from django.urls import reverse
from .models import NumeroLoteria
from .forms import NumeroLoteriaForm


# ============================================================
# PRUEBAS DE MODELO
# ============================================================

class NumeroLoteriaModelTest(TestCase):
    """Pruebas sobre el modelo NumeroLoteria: creacion, restricciones y unicidad."""

    def setUp(self):
        self.fecha_futura = date.today() + timedelta(days=7)
        self.datos_validos = {
            'numero': 4521,
            'propietario': 'Juan Perez',
            'fecha': self.fecha_futura,
            'estado': 'activo',
        }

    def test_cp001_crear_numero_valido(self):
        """CP-001: Registro exitoso con datos validos."""
        numero = NumeroLoteria.objects.create(**self.datos_validos)
        self.assertEqual(numero.numero, 4521)
        self.assertEqual(numero.propietario, 'Juan Perez')
        self.assertEqual(numero.fecha, self.fecha_futura)
        self.assertEqual(numero.estado, 'activo')

    def test_cp002_numero_valor_minimo(self):
        """CP-002: Numero con valor minimo (0000) se crea correctamente."""
        self.datos_validos['numero'] = 0
        numero = NumeroLoteria.objects.create(**self.datos_validos)
        self.assertEqual(numero.numero, 0)

    def test_cp003_numero_valor_maximo(self):
        """CP-003: Numero con valor maximo (9999) se crea correctamente."""
        self.datos_validos['numero'] = 9999
        numero = NumeroLoteria.objects.create(**self.datos_validos)
        self.assertEqual(numero.numero, 9999)

    def test_cp006_unicidad_numero_fecha(self):
        """CP-006: No se permite duplicar numero para la misma fecha (unique_together)."""
        NumeroLoteria.objects.create(**self.datos_validos)
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            NumeroLoteria.objects.create(**self.datos_validos)

    def test_cp007_mismo_numero_diferente_fecha(self):
        """CP-007: Mismo numero en fecha diferente es permitido."""
        NumeroLoteria.objects.create(**self.datos_validos)
        self.datos_validos['fecha'] = self.fecha_futura + timedelta(days=7)
        numero2 = NumeroLoteria.objects.create(**self.datos_validos)
        self.assertEqual(numero2.numero, 4521)

    def test_str_representacion(self):
        """Verifica la representacion en texto del modelo."""
        numero = NumeroLoteria.objects.create(**self.datos_validos)
        self.assertIn('4521', str(numero))
        self.assertIn('Juan Perez', str(numero))


# ============================================================
# PRUEBAS DE FORMULARIO
# ============================================================

class NumeroLoteriaFormTest(TestCase):
    """Pruebas sobre NumeroLoteriaForm: validaciones de campo y reglas de negocio."""

    def setUp(self):
        self.fecha_futura = date.today() + timedelta(days=7)
        self.datos_validos = {
            'numero': 4521,
            'propietario': 'Juan Perez',
            'fecha': self.fecha_futura,
        }

    def test_cp001_formulario_valido(self):
        """CP-001: Formulario con datos validos es aceptado."""
        form = NumeroLoteriaForm(data=self.datos_validos)
        self.assertTrue(form.is_valid())

    def test_cp002_numero_minimo_valido(self):
        """CP-002: Numero 0 es valido (limite inferior)."""
        self.datos_validos['numero'] = 0
        form = NumeroLoteriaForm(data=self.datos_validos)
        self.assertTrue(form.is_valid())

    def test_cp003_numero_maximo_valido(self):
        """CP-003: Numero 9999 es valido (limite superior)."""
        self.datos_validos['numero'] = 9999
        form = NumeroLoteriaForm(data=self.datos_validos)
        self.assertTrue(form.is_valid())

    def test_cp004_numero_mayor_9999_invalido(self):
        """CP-004: Numero mayor a 9999 es rechazado."""
        self.datos_validos['numero'] = 10000
        form = NumeroLoteriaForm(data=self.datos_validos)
        self.assertFalse(form.is_valid())
        self.assertIn('numero', form.errors)

    def test_cp005_numero_negativo_invalido(self):
        """CP-005: Numero negativo es rechazado."""
        self.datos_validos['numero'] = -1
        form = NumeroLoteriaForm(data=self.datos_validos)
        self.assertFalse(form.is_valid())
        self.assertIn('numero', form.errors)

    def test_cp006_numero_duplicado_misma_fecha(self):
        """CP-006: Numero duplicado para la misma fecha es rechazado por el formulario."""
        NumeroLoteria.objects.create(
            numero=4521,
            propietario='Maria Lopez',
            fecha=self.fecha_futura,
            estado='activo',
        )
        form = NumeroLoteriaForm(data=self.datos_validos)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Numero duplicado',
            str(form.errors)
        )

    def test_cp007_mismo_numero_fecha_diferente_valido(self):
        """CP-007: Mismo numero con fecha diferente es aceptado."""
        NumeroLoteria.objects.create(
            numero=4521,
            propietario='Maria Lopez',
            fecha=self.fecha_futura,
            estado='activo',
        )
        self.datos_validos['fecha'] = self.fecha_futura + timedelta(days=7)
        form = NumeroLoteriaForm(data=self.datos_validos)
        self.assertTrue(form.is_valid())

    def test_cp008b_fecha_pasada_rechazada(self):
        """CP-008b: Fecha de sorteo pasada es rechazada (FE-02)."""
        self.datos_validos['fecha'] = date.today() - timedelta(days=7)
        form = NumeroLoteriaForm(data=self.datos_validos)
        self.assertFalse(form.is_valid())
        self.assertIn('fecha', form.errors)

    def test_cp008_campos_vacios_rechazados(self):
        """CP-008: Campos obligatorios vacios son rechazados."""
        form = NumeroLoteriaForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('numero', form.errors)
        self.assertIn('propietario', form.errors)
        self.assertIn('fecha', form.errors)

    def test_cp008_propietario_vacio_rechazado(self):
        """CP-008: Propietario vacio es rechazado."""
        self.datos_validos['propietario'] = ''
        form = NumeroLoteriaForm(data=self.datos_validos)
        self.assertFalse(form.is_valid())
        self.assertIn('propietario', form.errors)


# ============================================================
# PRUEBAS DE VISTA
# ============================================================

class RegistrarNumeroViewTest(TestCase):
    """Pruebas sobre la vista registrar_numero: HTTP, redirecciones y mensajes."""

    def setUp(self):
        self.client = Client()
        self.url = reverse('loteria:registrar')
        self.fecha_futura = date.today() + timedelta(days=7)
        self.datos_validos = {
            'numero': 4521,
            'propietario': 'Juan Perez',
            'fecha': self.fecha_futura.isoformat(),
        }

    def test_cp009_get_muestra_formulario(self):
        """CP-009: Vista GET muestra formulario vacio."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'loteria/registrar.html')
        self.assertIsInstance(response.context['form'], NumeroLoteriaForm)

    def test_cp010_post_valido_redirige(self):
        """CP-010: Vista POST con datos validos redirige al listado."""
        response = self.client.post(self.url, data=self.datos_validos)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('loteria:listar'))

    def test_cp010_post_valido_crea_registro(self):
        """CP-010: Vista POST con datos validos crea el registro en BD."""
        self.client.post(self.url, data=self.datos_validos)
        self.assertEqual(NumeroLoteria.objects.count(), 1)
        numero = NumeroLoteria.objects.first()
        self.assertEqual(numero.numero, 4521)
        self.assertEqual(numero.propietario, 'Juan Perez')
        self.assertEqual(numero.estado, 'activo')

    def test_cp010_post_valido_muestra_mensaje_exito(self):
        """CP-010: Vista POST valido muestra mensaje de exito."""
        response = self.client.post(self.url, data=self.datos_validos, follow=True)
        self.assertContains(response, "Numero registrado exitosamente")

    def test_cp011_post_invalido_muestra_errores(self):
        """CP-011: Vista POST con numero invalido muestra errores en formulario."""
        datos_invalidos = self.datos_validos.copy()
        datos_invalidos['numero'] = 10000
        response = self.client.post(self.url, data=datos_invalidos)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())

    def test_cp011_post_campos_vacios(self):
        """CP-011: Vista POST con campos vacios no crea registro."""
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(NumeroLoteria.objects.count(), 0)

    def test_cp011b_post_fecha_pasada_rechazado(self):
        """CP-011b: Vista POST con fecha pasada no crea registro (FE-02)."""
        datos = self.datos_validos.copy()
        datos['fecha'] = (date.today() - timedelta(days=7)).isoformat()
        response = self.client.post(self.url, data=datos)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(NumeroLoteria.objects.count(), 0)
        self.assertContains(response, "fecha ya paso")

    def test_cp012_post_duplicado_muestra_error(self):
        """CP-012: Vista POST con numero duplicado muestra error."""
        NumeroLoteria.objects.create(
            numero=4521,
            propietario='Maria Lopez',
            fecha=self.fecha_futura,
            estado='activo',
        )
        response = self.client.post(self.url, data=self.datos_validos)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Numero duplicado")
        self.assertEqual(NumeroLoteria.objects.count(), 1)


# ============================================================
# PRUEBAS DE VISTA - CU-02: ACTUALIZAR NUMERO
# ============================================================

class ActualizarNumeroViewTest(TestCase):
    """Pruebas sobre la vista actualizar_numero: validacion de fecha, duplicado y flujo."""

    def setUp(self):
        self.client = Client()
        self.fecha_futura = date.today() + timedelta(days=7)
        self.fecha_pasada = date.today() - timedelta(days=7)
        self.numero_obj = NumeroLoteria.objects.create(
            numero=4521,
            propietario='Juan Perez',
            fecha=self.fecha_futura,
            estado='activo',
        )
        self.url = reverse('loteria:actualizar', args=[self.numero_obj.pk])
        self.datos_actualizados = {
            'numero': 4521,
            'propietario': 'Carlos Garcia',
            'fecha': self.fecha_futura.isoformat(),
        }

    def test_cp013_actualizacion_exitosa(self):
        """CP-013: Actualizacion exitosa con datos validos."""
        response = self.client.post(self.url, data=self.datos_actualizados, follow=True)
        self.assertContains(response, "Numero actualizado exitosamente")
        self.numero_obj.refresh_from_db()
        self.assertEqual(self.numero_obj.propietario, 'Carlos Garcia')

    def test_cp014_get_muestra_datos_actuales(self):
        """CP-014: Vista GET muestra formulario con datos actuales del registro."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'loteria/actualizar.html')
        form = response.context['form']
        self.assertEqual(form.initial['numero'], 4521)
        self.assertEqual(form.initial['propietario'], 'Juan Perez')

    def test_cp015_fecha_pasada_redirige_con_error(self):
        """CP-015: Si la fecha de sorteo ya paso, redirige con mensaje de error (FE-01)."""
        numero_pasado = NumeroLoteria.objects.create(
            numero=1234,
            propietario='Ana Ruiz',
            fecha=self.fecha_pasada,
            estado='activo',
        )
        url_pasado = reverse('loteria:actualizar', args=[numero_pasado.pk])
        response = self.client.get(url_pasado, follow=True)
        self.assertContains(response, "No se permite modificar")
        self.assertRedirects(
            self.client.get(url_pasado),
            reverse('loteria:listar')
        )

    def test_cp016_duplicado_nueva_fecha_rechazado(self):
        """CP-016: Duplicado al cambiar fecha genera error (FE-03)."""
        otra_fecha = self.fecha_futura + timedelta(days=7)
        NumeroLoteria.objects.create(
            numero=4521,
            propietario='Maria Lopez',
            fecha=otra_fecha,
            estado='activo',
        )
        datos = self.datos_actualizados.copy()
        datos['fecha'] = otra_fecha.isoformat()
        response = self.client.post(self.url, data=datos)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Numero duplicado")

    def test_cp017_numero_invalido_rechazado(self):
        """CP-017: Numero mayor a 9999 es rechazado en actualizacion (FE-02)."""
        datos = self.datos_actualizados.copy()
        datos['numero'] = 10000
        response = self.client.post(self.url, data=datos)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())

    def test_cp018_cambiar_fecha_a_pasada_rechazado(self):
        """CP-018: Cambiar la fecha a una pasada en el formulario es rechazado."""
        datos = self.datos_actualizados.copy()
        datos['fecha'] = self.fecha_pasada.isoformat()
        response = self.client.post(self.url, data=datos)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fecha ya paso")

    def test_cp019_actualizar_solo_propietario(self):
        """CP-019: Actualizar solo el propietario sin cambiar numero ni fecha."""
        datos = self.datos_actualizados.copy()
        datos['propietario'] = 'Pedro Martinez'
        response = self.client.post(self.url, data=datos, follow=True)
        self.assertContains(response, "Numero actualizado exitosamente")
        self.numero_obj.refresh_from_db()
        self.assertEqual(self.numero_obj.propietario, 'Pedro Martinez')
        self.assertEqual(self.numero_obj.numero, 4521)

    def test_cp020_registro_inexistente_404(self):
        """CP-020: Intentar actualizar un registro inexistente retorna 404."""
        url_inexistente = reverse('loteria:actualizar', args=[9999])
        response = self.client.get(url_inexistente)
        self.assertEqual(response.status_code, 404)


# ============================================================
# PRUEBAS DE VISTA - CU-03: ELIMINAR NUMERO
# ============================================================

class EliminarNumeroViewTest(TestCase):
    """Pruebas sobre la vista eliminar_numero: confirmacion, validacion de fecha y flujo."""

    def setUp(self):
        self.client = Client()
        self.fecha_futura = date.today() + timedelta(days=7)
        self.fecha_pasada = date.today() - timedelta(days=7)
        self.numero_obj = NumeroLoteria.objects.create(
            numero=4521,
            propietario='Juan Perez',
            fecha=self.fecha_futura,
            estado='activo',
        )
        self.url = reverse('loteria:eliminar', args=[self.numero_obj.pk])

    def test_cp021_eliminacion_exitosa(self):
        """CP-021: Eliminacion exitosa con confirmacion POST."""
        response = self.client.post(self.url, follow=True)
        self.assertContains(response, "Numero eliminado exitosamente")
        self.assertEqual(NumeroLoteria.objects.count(), 0)

    def test_cp022_get_muestra_confirmacion(self):
        """CP-022: Vista GET muestra datos del registro y solicita confirmacion."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'loteria/eliminar.html')
        self.assertContains(response, '4521')
        self.assertContains(response, 'Juan Perez')
        self.assertContains(response, 'Confirmar')

    def test_cp023_fecha_pasada_redirige_con_error(self):
        """CP-023: Si la fecha de sorteo ya paso, redirige con mensaje de error (FE-01)."""
        numero_pasado = NumeroLoteria.objects.create(
            numero=1234,
            propietario='Ana Ruiz',
            fecha=self.fecha_pasada,
            estado='activo',
        )
        url_pasado = reverse('loteria:eliminar', args=[numero_pasado.pk])
        response = self.client.get(url_pasado, follow=True)
        self.assertContains(response, "No se permite eliminar")
        # Verificar que no se elimino
        self.assertTrue(NumeroLoteria.objects.filter(pk=numero_pasado.pk).exists())

    def test_cp023_post_fecha_pasada_tambien_redirige(self):
        """CP-023: POST a registro con fecha pasada tambien redirige con error."""
        numero_pasado = NumeroLoteria.objects.create(
            numero=5678,
            propietario='Luis Torres',
            fecha=self.fecha_pasada,
            estado='activo',
        )
        url_pasado = reverse('loteria:eliminar', args=[numero_pasado.pk])
        response = self.client.post(url_pasado, follow=True)
        self.assertContains(response, "No se permite eliminar")
        self.assertTrue(NumeroLoteria.objects.filter(pk=numero_pasado.pk).exists())

    def test_cp024_cancelar_no_elimina(self):
        """CP-024: Acceder con GET (cancelar) no elimina el registro (FA-01)."""
        self.client.get(self.url)
        self.assertTrue(NumeroLoteria.objects.filter(pk=self.numero_obj.pk).exists())

    def test_cp025_registro_inexistente_404(self):
        """CP-025: Intentar eliminar un registro inexistente retorna 404."""
        url_inexistente = reverse('loteria:eliminar', args=[9999])
        response = self.client.get(url_inexistente)
        self.assertEqual(response.status_code, 404)

    def test_cp026_eliminado_no_aparece_en_listado(self):
        """CP-026: Registro eliminado ya no aparece en el listado."""
        self.client.post(self.url)
        response = self.client.get(reverse('loteria:listar'))
        self.assertNotContains(response, 'Juan Perez')


# ============================================================
# PRUEBAS DE VISTA - CU-04: LISTAR NUMEROS
# ============================================================

class ListarNumerosViewTest(TestCase):
    """Pruebas sobre la vista listar_numeros: listado completo, filtro y mensaje vacio."""

    def setUp(self):
        self.client = Client()
        self.url = reverse('loteria:listar')
        self.fecha1 = date.today() + timedelta(days=7)
        self.fecha2 = date.today() + timedelta(days=14)
        self.numero1 = NumeroLoteria.objects.create(
            numero=1234,
            propietario='Juan Perez',
            fecha=self.fecha1,
            estado='activo',
        )
        self.numero2 = NumeroLoteria.objects.create(
            numero=5678,
            propietario='Maria Lopez',
            fecha=self.fecha2,
            estado='activo',
        )

    def test_cp027_listar_todos(self):
        """CP-027: Listar todos los numeros registrados."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'loteria/listar.html')
        self.assertContains(response, 'Juan Perez')
        self.assertContains(response, 'Maria Lopez')
        self.assertContains(response, '1234')
        self.assertContains(response, '5678')

    def test_cp028_listar_sin_registros(self):
        """CP-028: Sin registros muestra mensaje 'No hay numeros registrados' (FE-01)."""
        NumeroLoteria.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No hay numeros registrados')

    def test_cp029_filtrar_por_fecha(self):
        """CP-029: Filtrar por fecha muestra solo los numeros de esa fecha (FA-01)."""
        response = self.client.get(self.url, {'fecha': self.fecha1.isoformat()})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Perez')
        self.assertNotContains(response, 'Maria Lopez')

    def test_cp030_filtrar_sin_resultados(self):
        """CP-030: Filtrar por fecha sin resultados muestra mensaje vacio."""
        fecha_sin_datos = (date.today() + timedelta(days=30)).isoformat()
        response = self.client.get(self.url, {'fecha': fecha_sin_datos})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No hay numeros registrados')

    def test_cp031_muestra_todos_los_campos(self):
        """CP-031: El listado muestra numero, propietario, fecha y estado (RN-01)."""
        response = self.client.get(self.url)
        # Verificar cabeceras de tabla
        self.assertContains(response, 'Numero')
        self.assertContains(response, 'Propietario')
        self.assertContains(response, 'Fecha')
        self.assertContains(response, 'Estado')
        # Verificar datos del primer registro
        self.assertContains(response, '1234')
        self.assertContains(response, 'Juan Perez')
        self.assertContains(response, 'Activo')
