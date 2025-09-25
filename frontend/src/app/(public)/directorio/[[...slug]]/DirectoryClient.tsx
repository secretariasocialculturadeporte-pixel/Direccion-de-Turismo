'use client';

import React, { useState, useEffect } from 'react';
import { useRouter, usePathname, useSearchParams } from 'next/navigation';
import { useDebounce } from '@/hooks/useDebounce';
import { Categoria } from '@/services/api';

export default function DirectoryClient({ categorias, initialSearchTerm }: { categorias: Categoria[], initialSearchTerm: string }) {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const [searchTerm, setSearchTerm] = useState(initialSearchTerm);
  const debouncedSearchTerm = useDebounce(searchTerm, 500);

  useEffect(() => {
    const current = new URLSearchParams(Array.from(searchParams.entries()));

    if (!debouncedSearchTerm) {
      current.delete('q');
    } else {
      current.set('q', debouncedSearchTerm);
    }

    const search = current.toString();
    const query = search ? `?${search}` : '';

    // Reemplazamos la URL en lugar de hacer push para no llenar el historial del navegador con cada letra tecleada
    router.replace(`${pathname}${query}`);
  }, [debouncedSearchTerm, pathname, router, searchParams]);

  const handleCategoryClick = (slug: string | null) => {
    const current = new URLSearchParams(Array.from(searchParams.entries()));
    let newPath = '/directorio';

    if (slug) {
      newPath = `/directorio/${slug}`;
    }

    const query = current.toString();
    router.push(`${newPath}${query ? `?${query}` : ''}`);
  };

  // Extraemos el slug actual para saber qué filtro está activo
  const activeSlug = pathname.split('/')[2] || null;

  return (
    <>
      <div className="w-full max-w-md mx-auto mb-8">
        <input
          type="text"
          placeholder="¿Qué estás buscando?"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-full shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div className="flex flex-wrap justify-center gap-2 mb-8">
        <button
          onClick={() => handleCategoryClick(null)}
          className={`px-4 py-2 rounded-full text-sm font-semibold ${!activeSlug ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'}`}
        >
          Todos
        </button>
        {categorias.map((cat) => (
          <button
            key={cat.id}
            onClick={() => handleCategoryClick(cat.slug)}
            className={`px-4 py-2 rounded-full text-sm font-semibold ${activeSlug === cat.slug ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'}`}
          >
            {cat.nombre}
          </button>
        ))}
      </div>
    </>
  );
}