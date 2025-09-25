"use client";

import Link from 'next/link';
import { useState } from 'react';

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const navLinks = [
    { name: 'El Municipio', href: '/municipio' },
    { name: 'Directorio Turístico', href: '/directorio' },
    { name: 'Artesanos', href: '/directorio/artesanos' },
    { name: 'Atractivos', href: '/atractivos' },
    { name: 'Agenda Cultural', href: '/agenda-cultural' },
    { name: 'Noticias', href: '/noticias' },
    { name: 'Blog', href: '/blog' },
    { name: 'Mapa', href: '/mapa' },
  ];

  return (
    <header className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex-shrink-0">
            <Link href="/" className="text-2xl font-bold text-indigo-600">
              Turismo Gaitán
            </Link>
          </div>

          {/* Navegación para Desktop */}
          <nav className="hidden md:flex md:space-x-8">
            {navLinks.map((link) => (
              <Link key={link.name} href={link.href} className="text-gray-500 hover:text-gray-900 font-medium">
                {link.name}
              </Link>
            ))}
          </nav>

          {/* Botón de Login para Desktop */}
          <div className="hidden md:block">
            <Link href="/login" className="px-4 py-2 bg-gray-100 text-gray-700 hover:bg-gray-200 rounded-md font-semibold text-sm">
              Acceso Prestadores
            </Link>
          </div>

          {/* Botón de Menú para Móvil */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
            >
              <span className="sr-only">Abrir menú principal</span>
              {/* Icono de hamburguesa */}
              <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d={!isMenuOpen ? 'M4 6h16M4 12h16M4 18h16' : 'M6 18L18 6M6 6l12 12'} />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Menú desplegable para Móvil */}
      {isMenuOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            {navLinks.map((link) => (
              <Link key={link.name} href={link.href} className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50">
                {link.name}
              </Link>
            ))}
          </div>
          <div className="pt-4 pb-3 border-t border-gray-200">
            <div className="px-2">
              <Link href="/login" className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50">
                Acceso Prestadores
              </Link>
            </div>
          </div>
        </div>
      )}
    </header>
  );
}