from api.models import CustomUser, CategoriaPrestador, PrestadorServicio

# --- Create a User to own the Prestador ---
# get_or_create to avoid errors on subsequent runs
user, created = CustomUser.objects.get_or_create(
    username='prestador_test',
    defaults={'role': CustomUser.Role.PRESTADOR, 'email': 'test@example.com'}
)
if created:
    user.set_password('testpassword')
    user.save()
    print("Test user created.")

# --- Create a Category ---
categoria, created = CategoriaPrestador.objects.get_or_create(
    nombre='Hoteles',
    defaults={'slug': 'hoteles'}
)
if created:
    print("Category 'Hoteles' created.")

# --- Create a Service Provider ---
prestador, created = PrestadorServicio.objects.get_or_create(
    usuario=user,
    defaults={
        'nombre_negocio': 'Hotel Paraíso Natural',
        'categoria': categoria,
        'descripcion': 'Un hermoso hotel para disfrutar de la naturaleza.',
        'telefono': '123456789',
        'aprobado': True  # This is crucial for the public API
    }
)
if created:
    print("Approved service provider 'Hotel Paraíso Natural' created.")
else:
    # Ensure it's approved if it already existed
    if not prestador.aprobado:
        prestador.aprobado = True
        prestador.save()
        print("Service provider was found and set to 'approved'.")

print("Sample data creation/verification complete.")