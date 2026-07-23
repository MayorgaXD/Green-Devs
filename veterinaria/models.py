from django.db import models

# Create your models here.
from django.db import models

# Opciones para el Nivel Académico / Experiencia del Especialista
class NivelAcademico(models.TextChoices):
    BASICO = 'BASICO', 'Nivel Básico'
    INTERMEDIO = 'INTERMEDIO', 'Nivel Intermedio'
    ALTO = 'ALTO', 'Nivel Alto'
    ESPECIALIZADO = 'ESPECIALIZADO', 'Especializado'
    EXPERTO = 'EXPERTO', 'Veterinario Experto'


# Modelo Base Abstracto (Características compartidas que heredan ambos)
class PersonaBase(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre Completo")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    edad = models.PositiveIntegerField(verbose_name="Edad")
    ubicacion_gps = models.CharField(
        max_length=255, 
        help_text="Coordenadas GPS o Dirección de estancia/vivienda",
        verbose_name="Ubicación de Estancia / Vivienda"
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True  # solo sirve para heredar atributos


# Modelo para el Público / Usuarios Ganaderos
class Usuario(PersonaBase):
    nombre_finca = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre de la Finca/Estancia")

    class Meta:
        verbose_name = "Usuario Ganadero"
        verbose_name_plural = "Usuarios Ganaderos"

    def __str__(self):
        return f"Ganadero: {self.nombre} - {self.email}"


# Modelo para Profesionales / Especialistas Veterinarios
class Especialista(PersonaBase):
    lugar_estudios = models.CharField(max_length=200, verbose_name="Universidad / Centro de Estudios")
    grado_especialidad = models.CharField(
        max_length=150, 
        help_text="Ejemplo: Cirugía Bovina, Nutrición Animal, Reproducción",
        verbose_name="Grado de Especialidad"
    )
    experiencia_laboral = models.TextField(
        blank=True, 
        null=True, 
        help_text="Resumen o años de experiencia en campo",
        verbose_name="Experiencia Laboral"
    )
    nivel_academico = models.CharField(
        max_length=20,
        choices=NivelAcademico.choices,
        default=NivelAcademico.BASICO,
        verbose_name="Nivel Académico / Experiencia"
    )

    class Meta:
        verbose_name = "Especialista Veterinario"
        verbose_name_plural = "Especialistas Veterinarios"

    def __str__(self):
        return f"Dr(a). {self.nombre} - {self.get_nivel_academico_display()}"