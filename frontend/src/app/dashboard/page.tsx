"use client";

import React, { useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import ProfileForm from '@/components/ProfileForm';

export default function DashboardPage() {
  const { isAuthenticated, isLoading, logout } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // Si la autenticación ha terminado de cargar y el usuario no está autenticado,
    // lo redirigimos a la página de login.
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  // Muestra un estado de carga mientras se verifica la autenticación
  if (isLoading || !isAuthenticated) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p>Cargando...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="flex justify-between items-center px-4 py-6 mx-auto max-w-7xl sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold leading-tight text-gray-900">
            Panel de Control del Prestador
          </h1>
          <button
            onClick={logout}
            className="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            Cerrar Sesión
          </button>
        </div>
      </header>
      <main>
        <div className="py-6 mx-auto max-w-7xl sm:px-6 lg:px-8">
          <div className="px-4 py-4 bg-white rounded-lg shadow sm:px-0">
            <div className="p-8 border-4 border-gray-200 border-dashed rounded-lg">
              <div className="p-6">
                <h2 className="text-2xl font-bold mb-4">Gestiona tu Perfil</h2>
                <p className="mb-6 text-gray-600">
                  Completa y actualiza la información de tu negocio. Los campos que completes aquí serán visibles en el portal público una vez que tu perfil sea aprobado por un administrador.
                </p>
                <ProfileForm />
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}