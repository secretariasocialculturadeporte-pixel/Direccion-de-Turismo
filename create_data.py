from api.models import CustomUser, CategoriaPrestador, PrestadorServicio

print("Starting data creation script...")

# --- Lista de categorías a crear ---
categorias_a_crear = {
    'restaurantes': 'Restaurantes',
    'hoteles': 'Hoteles',
    'cabanas': 'Cabañas',
    'ecohoteles': 'Ecohoteles',
    'piscinas-centros-recreacionales': 'Piscinas y Centros Recreacionales',
    'bares': 'Bares',
    'discotecas': 'Discotecas',
    'guias-turisticos': 'Guías Turísticos',
    'asociacion-de-guias': 'Asociación de Guías',
    'agencia-viajes-mayoristas': 'Agencia de Viajes Mayorista',
    'agencia-viajes-operativas': 'Agencia de Viajes Operativa',
    'agencia-viajes-receptivas': 'Agencia de Viajes Receptiva',
    'transporte-terrestre': 'Transporte Terrestre',
    'transporte-aereo': 'Transporte Aéreo',
    'transporte-maritimo': 'Transporte Marítimo',
    'artesanos': 'Artesanos'
}

# --- Crear cada categoría ---
for slug, nombre in categorias_a_crear.items():
    cat, created = CategoriaPrestador.objects.get_or_create(
        slug=slug,
        defaults={'nombre': nombre}
    )
    if created:
        print(f"Category '{nombre}' created.")

# --- Crear un usuario de prueba para el prestador de servicios ---
user_prestador, created = CustomUser.objects.get_or_create(
    username='prestador_test',
    defaults={'role': CustomUser.Role.PRESTADOR, 'email': 'prestador@example.com'}
)
if created:
    user_prestador.set_password('testpassword')
    user_prestador.save()
    print("Test user 'prestador_test' created.")

# --- Crear un segundo usuario de prueba para el artesano ---
user_artesano, created = CustomUser.objects.get_or_create(
    username='artesano_test',
    defaults={'role': CustomUser.Role.PRESTADOR, 'email': 'artesano@example.com'}
)
if created:
    user_artesano.set_password('testpassword')
    user_artesano.save()
    print("Test user 'artesano_test' created.")

# --- Crear un prestador de servicio de ejemplo (Hotel) ---
categoria_hotel = CategoriaPrestador.objects.get(slug='hoteles')
prestador_hotel, created = PrestadorServicio.objects.get_or_create(
    usuario=user_prestador,
    defaults={
        'nombre_negocio': 'Hotel El Descanso Llanero',
        'categoria': categoria_hotel,
        'descripcion': 'El mejor lugar para descansar en su viaje por los llanos.',
        'telefono': '3101234567',
        'aprobado': True
    }
)
if created:
    print("Approved service provider 'Hotel El Descanso Llanero' created.")
else:
    if not prestador_hotel.aprobado:
        prestador_hotel.aprobado = True
        prestador_hotel.save()
        print("Service provider 'Hotel El Descanso Llanero' set to approved.")

# --- Crear un artesano de ejemplo ---
categoria_artesano = CategoriaPrestador.objects.get(slug='artesanos')
artesano_ejemplo, created = PrestadorServicio.objects.get_or_create(
    usuario=user_artesano,
    defaults={
        'nombre_negocio': 'Artesanías El Capibara de Oro',
        'categoria': categoria_artesano,
        'descripcion': 'Auténticas artesanías de la región, hechas a mano con amor.',
        'telefono': '3119876543',
        'aprobado': True
    }
)
if created:
    print("Approved artisan 'Artesanías El Capibara de Oro' created.")
else:
    if not artesano_ejemplo.aprobado:
        artesano_ejemplo.aprobado = True
        artesano_ejemplo.save()
        print("Artisan 'Artesanías El Capibara de Oro' set to approved.")

print("Sample data creation/verification complete.")