import React, { Suspense } from 'react';
import Link from 'next/link';
import { getCategorias, getPrestadores, Categoria, PrestadorPublico } from '@/services/api';
import DirectoryClient from './DirectoryClient'; // Componente cliente para la interactividad

// --- Componente de Esqueleto para la Tarjeta ---
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

// --- Componente de la Tarjeta del Prestador ---
function PrestadorCard({ prestador }: { prestador: PrestadorPublico }) {
  // El detalle de un artesano o de un prestador usa la misma página de detalle
  return (
    <Link href={`/oferta/${prestador.id}`} legacyBehavior>
      <a className="border rounded-lg shadow-md hover:shadow-xl transition-shadow overflow-hidden group">
        <div className="relative w-full h-48">
          {prestador.imagen_principal ? (
            <img
              src={prestador.imagen_principal}
              alt={`Imagen de ${prestador.nombre_negocio}`}
              className="w-full h-full object-cover transition-transform group-hover:scale-110"
            />
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
  );
}


// --- Componente Principal de la Página (Server Component) ---
export default async function DirectorioPage({ params, searchParams }: {
  params: { slug?: string[] };
  searchParams: { [key: string]: string | string[] | undefined };
}) {
  const categoriaSlug = params.slug?.[0];
  const searchTerm = typeof searchParams.q === 'string' ? searchParams.q : undefined;

  // Lógica de carga de datos
  const allCategoriasPromise = getCategorias();

  let prestadoresPromise;
  let pageTitle: string;
  let categoriasParaFiltro: Categoria[];

  // Si estamos en la página de artesanos, solo mostramos artesanos
  if (categoriaSlug === 'artesanos') {
    prestadoresPromise = getPrestadores('artesanos', searchTerm);
    pageTitle = 'Directorio de Artesanos';
    // No mostramos otros filtros en la página de artesanos
    categoriasParaFiltro = [];
  } else {
    // Para el directorio principal y otras categorías, excluimos a los artesanos
    prestadoresPromise = getPrestadores(categoriaSlug, searchTerm, 'artesanos');
    const allCategorias = await allCategoriasPromise;
    const activeCategory = categoriaSlug ? allCategorias.find(c => c.slug === categoriaSlug) : null;
    pageTitle = activeCategory ? `Directorio: ${activeCategory.nombre}` : 'Directorio Turístico';
    // Excluimos a los artesanos de las opciones de filtro
    categoriasParaFiltro = allCategorias.filter(c => c.slug !== 'artesanos');
  }

  const [prestadores, allCategorias] = await Promise.all([prestadoresPromise, allCategoriasPromise]);

  // Si estamos en la página de artesanos, no necesitamos recalcular las categorías de filtro
  if (categoriaSlug !== 'artesanos') {
      categoriasParaFiltro = allCategorias.filter(c => c.slug !== 'artesanos');
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold text-center mb-4">{pageTitle}</h1>

      {/* El componente cliente solo se muestra si hay categorías para filtrar */}
      {categoriasParaFiltro.length > 0 && (
          <DirectoryClient categorias={categoriasParaFiltro} initialSearchTerm={searchTerm || ''} />
      )}

      {/* Grid de Prestadores */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mt-8">
        <Suspense fallback={<p>Cargando resultados...</p>}>
          {prestadores.length > 0 ? (
            prestadores.map((prestador) => (
              <PrestadorCard key={prestador.id} prestador={prestador} />
            ))
          ) : (
            <p className="text-center col-span-full">No se encontraron resultados para tu búsqueda.</p>
          )}
        </Suspense>
      </div>
    </div>
  );
}