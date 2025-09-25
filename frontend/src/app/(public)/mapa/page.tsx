"use client";

import React from 'react';
import MapComponent from '@/components/MapComponent';

export default function MapaPage() {
  return (
    <div className="py-12 bg-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
            Mapa Interactivo de Puerto Gaitán
          </h1>
          <p className="mt-4 text-lg text-gray-600">
            Explora, filtra y descubre todos los puntos de interés de nuestro municipio en un solo lugar.
          </p>
        </div>

        <div className="bg-white p-4 rounded-lg shadow-xl">
          <MapComponent />
        </div>
      </div>
    </div>
  );
}