'use client';

import React, { useState, useEffect, Suspense } from 'react';
import Link from 'next/link';
import { getPrestadores, PrestadorPublico } from '@/services/api';
import { useDebounce } from '@/hooks/useDebounce';

// Reutilizamos el componente de esqueleto para la tarjeta del prestador
function PrestadorCardSkeleton() {
  return (
    <div className="border rounded-lg shadow-md animate-pulse">
      <div className="w-full h-48 bg-gray-300 rounded-t-lg"></div>
      <div className="p-4">
        <div className="h-6 bg-gray-300 rounded w-3/4 mb-2"></div>
        <div className="h-4 bg-gray-300 rounded w-1/2"></div>
      </div>
    </div>
  );
}

// Componente principal para la página de Artesanos
function ArtesanosContent() {
  const [artesanos, setArtesanos] = useState<PrestadorPublico[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const debouncedSearchTerm = useDebounce(searchTerm, 500);

  useEffect(() => {
    async function loadArtesanos() {
      try {
        setLoading(true);
        // Hacemos la llamada a la API filtrando directamente por la categoría 'artesanos'
        const fetchedArtesanos = await getPrestadores('artesanos', debouncedSearchTerm);
        setArtesanos(fetchedArtesanos);
        setError(null);
      } catch (err) {
        setError('No se pudo cargar la información de los artesanos. Por favor, inténtalo de nuevo más tarde.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadArtesanos();
  }, [debouncedSearchTerm]);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold text-center mb-4">Directorio de Artesanos</h1>
      <p className="text-center text-gray-600 mb-8">Descubre el talento y la creatividad de los artesanos de nuestra región.</p>

      {/* Barra de Búsqueda */}
      <div className="w-full max-w-md mx-auto mb-8">
        <input
          type="text"
          placeholder="Buscar artesano por nombre..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-full shadow-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
        />
      </div>

      {error && <p className="text-center text-red-500">{error}</p>}

      {/* Grid de Artesanos */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {loading ? (
          Array.from({ length: 4 }).map((_, index) => <PrestadorCardSkeleton key={index} />)
        ) : artesanos.length > 0 ? (
          artesanos.map((artesano) => (
            // El enlace sigue apuntando a la página de detalle genérica
            <Link key={artesano.id} href={`/oferta/${artesano.id}`} legacyBehavior>
              <a className="border rounded-lg shadow-md hover:shadow-xl transition-shadow overflow-hidden group">
                <div className="relative w-full h-48">
                  {artesano.imagen_principal ? (
                    <img src={artesano.imagen_principal} alt={`Imagen de ${artesano.nombre_negocio}`} className="w-full h-full object-cover transition-transform group-hover:scale-110" />
                  ) : (
                    <div className="w-full h-full bg-gray-200 flex items-center justify-center">
                      <span className="text-gray-500">Sin imagen</span>
                    </div>
                  )}
                </div>
                <div className="p-4">
                  <h3 className="text-lg font-bold">{artesano.nombre_negocio}</h3>
                  <p className="text-sm text-amber-700">{artesano.categoria_nombre}</p>
                </div>
              </a>
            </Link>
          ))
        ) : (
          <p className="text-center col-span-full">No se encontraron artesanos que coincidan con tu búsqueda.</p>
        )}
      </div>
    </div>
  );
}

export default function ArtesanosPage() {
    return (
        <Suspense fallback={<div>Cargando directorio de artesanos...</div>}>
            <ArtesanosContent />
        </Suspense>
    )
}