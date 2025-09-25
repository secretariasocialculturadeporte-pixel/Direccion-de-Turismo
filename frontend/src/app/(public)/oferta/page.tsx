'use client';

import React, { useState, useEffect, Suspense } from 'react';
import Link from 'next/link';
import { getCategorias, getPrestadores, Categoria, PrestadorPublico } from '@/services/api';

// Un componente de esqueleto para la tarjeta del prestador
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

// El componente principal de la página
function OfertaContent() {
  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [prestadores, setPrestadores] = useState<PrestadorPublico[]>([]);
  const [selectedCategoria, setSelectedCategoria] = useState<string | undefined>(undefined);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadInitialData() {
      try {
        setLoading(true);
        const [fetchedCategorias, fetchedPrestadores] = await Promise.all([
          getCategorias(),
          getPrestadores(),
        ]);
        setCategorias(fetchedCategorias);
        setPrestadores(fetchedPrestadores);
        setError(null);
      } catch (err) {
        setError('No se pudo cargar la información. Por favor, inténtalo de nuevo más tarde.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadInitialData();
  }, []);

  useEffect(() => {
    async function loadPrestadores() {
      try {
        setLoading(true);
        const fetchedPrestadores = await getPrestadores(selectedCategoria);
        setPrestadores(fetchedPrestadores);
        setError(null);
      } catch (err) {
        setError('No se pudo cargar los prestadores. Por favor, inténtalo de nuevo.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    // No ejecutamos esto en la carga inicial, solo cuando cambia la categoría seleccionada
    if (selectedCategoria !== undefined) {
      loadPrestadores();
    }
  }, [selectedCategoria]);

  const handleCategoriaClick = (slug: string | undefined) => {
    setSelectedCategoria(slug);
    // Si el slug es undefined, volvemos a cargar todos
    if (slug === undefined) {
      setLoading(true);
      getPrestadores()
        .then(setPrestadores)
        .catch(() => setError('Error al recargar los prestadores.'))
        .finally(() => setLoading(false));
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold text-center mb-8">Oferta Turística</h1>

      {/* Filtros de Categoría */}
      <div className="flex flex-wrap justify-center gap-2 mb-8">
        <button
          onClick={() => handleCategoriaClick(undefined)}
          className={`px-4 py-2 rounded-full text-sm font-semibold ${!selectedCategoria ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'}`}
        >
          Todos
        </button>
        {categorias.map((cat) => (
          <button
            key={cat.id}
            onClick={() => handleCategoriaClick(cat.slug)}
            className={`px-4 py-2 rounded-full text-sm font-semibold ${selectedCategoria === cat.slug ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'}`}
          >
            {cat.nombre}
          </button>
        ))}
      </div>

      {error && <p className="text-center text-red-500">{error}</p>}

      {/* Grid de Prestadores */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {loading ? (
          // Mostrar esqueletos mientras carga
          Array.from({ length: 8 }).map((_, index) => <PrestadorCardSkeleton key={index} />)
        ) : prestadores.length > 0 ? (
          prestadores.map((prestador) => (
            <Link key={prestador.id} href={`/oferta/${prestador.id}`} legacyBehavior>
              <a className="border rounded-lg shadow-md hover:shadow-xl transition-shadow overflow-hidden group">
                <div className="relative w-full h-48">
                  {prestador.imagen_principal ? (
                    <img src={prestador.imagen_principal} alt={`Imagen de ${prestador.nombre_negocio}`} className="w-full h-full object-cover transition-transform group-hover:scale-110" />
                  ) : (
                    <div className="w-full h-full bg-gray-200 flex items-center justify-center">
                      <span className="text-gray-500">Sin imagen</span>
                    </div>
                  )}
                </div>
                <div className="p-4">
                  <h3 className="text-lg font-bold">{prestador.nombre_negocio}</h3>
                  <p className="text-sm text-gray-600">{prestador.categoria_nombre}</p>
                </div>
              </a>
            </Link>
          ))
        ) : (
          <p className="text-center col-span-full">No se encontraron prestadores en esta categoría.</p>
        )}
      </div>
    </div>
  );
}

export default function OfertaPage() {
    return (
        <Suspense fallback={<div>Cargando...</div>}>
            <OfertaContent />
        </Suspense>
    )
}