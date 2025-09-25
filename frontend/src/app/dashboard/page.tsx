"use client";

"use client";

import React, { useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import ProfileForm from '@/components/ProfileForm';
import AdminDashboard from '@/components/AdminDashboard'; // Lo crearemos a continuación

// Componente para el panel del prestador
const PrestadorDashboard = () => (
  <>
    <h1 className="text-3xl font-bold leading-tight text-gray-900">
      Panel de Control del Prestador
    </h1>
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
  </>
);

// Componente para el panel de administración
const AdminPanel = () => (
  <>
    <h1 className="text-3xl font-bold leading-tight text-gray-900">
      Panel de Administración
    </h1>
    <main>
      <div className="py-6 mx-auto max-w-7xl sm:px-6 lg:px-8">
        <AdminDashboard />
      </div>
    </main>
  </>
);

export default function DashboardPage() {
  const { user, isAuthenticated, isLoading, logout } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading || !user) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p>Cargando...</p>
      </div>
    );
  }

  const renderDashboard = () => {
    switch (user.role) {
      case 'PRESTADOR':
        return <PrestadorDashboard />;
      case 'ADMIN':
      case 'FUNCIONARIO':
        return <AdminPanel />;
      default:
        return <p>No tienes acceso a este panel.</p>;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="flex justify-between items-center px-4 py-6 mx-auto max-w-7xl sm:px-6 lg:px-8">
          {renderDashboard()}
          <button
            onClick={logout}
            className="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            Cerrar Sesión
          </button>
        </div>
      </header>
    </div>
  );
}