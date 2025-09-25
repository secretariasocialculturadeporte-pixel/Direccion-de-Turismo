import React, { Suspense } from 'react';
import Link from 'next/link';
import { getPrestadorById } from '@/services/api';
import { notFound } from 'next/navigation';

// Componente para mostrar la información de contacto de forma limpia
const ContactItem = ({ label, value, href }: { label: string, value?: string | null, href?: string | null }) => {
  if (!value) return null;

  const content = href ? (
    <a href={href} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
      {value}
    </a>
  ) : (
    <span>{value}</span>
  );

  return (
    <li className="flex justify-between py-2 border-b">
      <span className="font-bold text-gray-700">{label}:</span>
      <span className="text-gray-800 text-right">{content}</span>
    </li>
  );
};


// --- Componente Principal de la Página (Server Component) ---
export default async function PrestadorDetailPage({ params }: { params: { id: string } }) {
  const id = parseInt(params.id, 10);

  if (isNaN(id)) {
    notFound(); // Si el ID no es un número, muestra un 404
  }

  try {
    const prestador = await getPrestadorById(id);

    return (
      <div className="container mx-auto px-4 py-8">
        {/* Encabezado */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold">{prestador.nombre_negocio}</h1>
          <p className="text-xl text-gray-600 mt-2">{prestador.categoria.nombre}</p>
        </div>

        {/* Galería de Imágenes */}
        {prestador.galeria_imagenes && prestador.galeria_imagenes.length > 0 && (
          <div className="mb-8">
            <h2 className="text-2xl font-semibold mb-4">Galería</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {prestador.galeria_imagenes.map((img) => (
                <div key={img.id} className="overflow-hidden rounded-lg shadow-md">
                  <img
                    src={img.imagen}
                    alt={img.alt_text || `Imagen de ${prestador.nombre_negocio}`}
                    className="w-full h-full object-cover"
                  />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Contenido Principal */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-2">
            <h2 className="text-2xl font-semibold border-b pb-2 mb-4">Descripción</h2>
            <p className="text-gray-700 whitespace-pre-wrap">{prestador.descripcion || 'No hay descripción disponible.'}</p>

            {prestador.promociones_ofertas && (
              <>
                <h2 className="text-2xl font-semibold border-b pb-2 mt-8 mb-4">Promociones y Ofertas</h2>
                <p className="text-gray-700 whitespace-pre-wrap">{prestador.promociones_ofertas}</p>
              </>
            )}
          </div>

          {/* Información de Contacto */}
          <div className="bg-gray-50 p-6 rounded-lg shadow-sm h-fit">
            <h2 className="text-2xl font-semibold border-b pb-2 mb-4">Contacto</h2>
            <ul className="space-y-1">
                <ContactItem label="Teléfono" value={prestador.telefono} href={`tel:${prestador.telefono}`} />
                <ContactItem label="Email" value={prestador.email_contacto} href={`mailto:${prestador.email_contacto}`} />
                <ContactItem label="Ubicación" value={prestador.ubicacion_mapa} />
                <ContactItem label="WhatsApp" value={prestador.red_social_whatsapp} href={`https://wa.me/${prestador.red_social_whatsapp}`} />
                <ContactItem label="Facebook" value="Visitar perfil" href={prestador.red_social_facebook} />
                <ContactItem label="Instagram" value="Visitar perfil" href={prestador.red_social_instagram} />
            </ul>
          </div>
        </div>

        <div className="text-center mt-12">
          <Link href="/directorio" legacyBehavior>
            <a className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors">
              &larr; Volver al Directorio
            </a>
          </Link>
        </div>
      </div>
    );
  } catch (error) {
    // Si la API no encuentra el prestador, getPrestadorById debería lanzar un error
    // que podemos capturar para mostrar una página 404.
    console.error("Error fetching prestador:", error);
    notFound();
  }
}