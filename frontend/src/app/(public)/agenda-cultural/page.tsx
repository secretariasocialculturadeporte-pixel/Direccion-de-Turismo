"use client";

import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import Link from 'next/link';

const API_BASE_URL = 'http://localhost:8000/api';

interface Evento {
  id: number;
  titulo: string;
  slug: string;
  subcategoria_evento: 'FESTIVAL_PRINCIPAL' | 'CELEBRACION_LLANERIDAD' | 'ACTIVIDAD_CIVICA' | 'OTRO';
  fecha_evento_inicio: string;
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  // Formato "15 de Septiembre"
  return date.toLocaleDateString('es-CO', {
    day: 'numeric',
    month: 'long',
  });
};

const SectionCard = ({ title, events }: { title: string, events: Evento[] }) => (
  <div className="bg-white rounded-2xl shadow-lg p-6 md:p-8">
    <h2 className="text-2xl font-bold text-indigo-700 mb-6 border-b-2 border-indigo-200 pb-3">{title}</h2>
    <ul className="space-y-4">
      {events.map(evento => (
        <li key={evento.id} className="flex items-center space-x-4">
          <div className="flex-shrink-0 bg-indigo-100 text-indigo-800 rounded-lg w-20 h-14 flex flex-col items-center justify-center text-center font-bold">
            <span className="text-xs uppercase">{new Date(evento.fecha_evento_inicio).toLocaleString('es-CO', { month: 'short' })}</span>
            <span className="text-2xl">{new Date(evento.fecha_evento_inicio).getDate()}</span>
          </div>
          <div className="flex-grow">
            <Link href={`/publicaciones/${evento.slug}`} className="font-semibold text-gray-800 hover:text-indigo-600 transition-colors">
              {evento.titulo}
            </Link>
          </div>
        </li>
      ))}
    </ul>
  </div>
);

export default function AgendaCulturalPage() {
  const [eventos, setEventos] = useState<Evento[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchEventos = async () => {
      setIsLoading(true);
      try {
        const response = await axios.get(`${API_BASE_URL}/publicaciones/`, {
          params: { tipo: 'EVENTO' },
        });
        // Ordenar por fecha de inicio
        const sortedEventos = response.data.sort((a: Evento, b: Evento) =>
          new Date(a.fecha_evento_inicio).getTime() - new Date(b.fecha_evento_inicio).getTime()
        );
        setEventos(sortedEventos);
      } catch (err) {
        setError('No se pudo cargar la agenda cultural. Por favor, intente de nuevo más tarde.');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchEventos();
  }, []);

  const { festivales, llaneridad, civicas } = useMemo(() => {
    return {
      festivales: eventos.filter(e => e.subcategoria_evento === 'FESTIVAL_PRINCIPAL'),
      llaneridad: eventos.filter(e => e.subcategoria_evento === 'CELEBRACION_LLANERIDAD'),
      civicas: eventos.filter(e => e.subcategoria_evento === 'ACTIVIDAD_CIVICA'),
    };
  }, [eventos]);

  return (
    <div className="py-12 bg-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl">
            Agenda Cultural y Turística
          </h1>
          <p className="mt-4 text-xl text-gray-600">
            El calendario de eventos, ferias y celebraciones que hacen vibrar a Puerto Gaitán.
          </p>
        </div>

        {isLoading ? (
          <p className="text-center">Cargando agenda...</p>
        ) : error ? (
          <p className="text-center text-red-500">{error}</p>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
            <div className="lg:col-span-2 space-y-8">
              <SectionCard title="Festivales y Eventos Principales" events={festivales} />
              <SectionCard title="Actividades Culturales y Cívicas Anuales" events={civicas} />
            </div>
            <div className="lg:col-span-1 space-y-8">
              <SectionCard title="Celebraciones de la Llaneridad" events={llaneridad} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}