"use client";

import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

interface Contenido {
  id: number;
  seccion: string;
  titulo: string;
  contenido: string;
  orden: number;
}

export default function SecretariaTurismoPage() {
  const [contenidos, setContenidos] = useState<Contenido[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchContenidoSecretaria = useCallback(async () => {
    setIsLoading(true);
    try {
      // Obtenemos todo el contenido y lo filtramos en el frontend.
      const response = await axios.get(`${API_BASE_URL}/contenido-municipio/`);
      const filteredContent = response.data.results.filter(
        (item: Contenido) => item.seccion === 'SECRETARIA_TURISMO'
      );
      setContenidos(filteredContent);
    } catch (err) {
      setError('No se pudo cargar la información de la Secretaría. Por favor, inténtelo de nuevo más tarde.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchContenidoSecretaria();
  }, [fetchContenidoSecretaria]);

  if (isLoading) return <p className="text-center py-10">Cargando información...</p>;
  if (error) return <p className="text-center text-red-500 py-10">{error}</p>;

  return (
    <div className="bg-gray-50 py-12">
      <div className="container mx-auto px-4">
        <header className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900">
            Secretaría de Turismo y Desarrollo Económico
          </h1>
          <p className="mt-4 text-xl text-gray-600">
            Conoce la estructura y el trabajo detrás del impulso turístico de Puerto Gaitán.
          </p>
        </header>

        <div className="max-w-4xl mx-auto">
          <div className="space-y-10">
            {contenidos.length > 0 ? (
              contenidos.map(item => (
                <article key={item.id} className="bg-white p-8 rounded-xl shadow-lg transition-shadow hover:shadow-2xl">
                  <h2 className="text-3xl font-bold text-gray-800 mb-4">{item.titulo}</h2>
                  <div className="prose prose-lg max-w-none text-gray-700 whitespace-pre-wrap">
                    {item.contenido}
                  </div>
                </article>
              ))
            ) : (
              <p className="text-center text-gray-500">No hay información disponible en este momento.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}