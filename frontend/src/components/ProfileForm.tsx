"use client";

import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { useAuth } from '@/contexts/AuthContext';
import ImageGalleryManager from './ImageGalleryManager';
import DocumentManager from './DocumentManager';

const API_BASE_URL = 'http://localhost:8000/api';

// Definimos los tipos para los datos que vienen del backend
interface Image {
  id: number;
  imagen: string;
  alt_text: string;
}

interface Document {
  id: number;
  documento: string;
  nombre_documento: string;
  fecha_subida: string;
}

interface ProfileData {
  nombre_negocio: string;
  descripcion: string;
  telefono: string;
  email_contacto: string;
  red_social_facebook: string;
  red_social_instagram: string;
  red_social_whatsapp: string;
  ubicacion_mapa: string;
  promociones_ofertas: string;
  reporte_ocupacion_nacional: number;
  reporte_ocupacion_internacional: number;
  categoria_nombre: string;
  aprobado: boolean;
  galeria_imagenes: Image[];
  documentos_legalizacion: Document[];
}

export default function ProfileForm() {
  const { token } = useAuth();
  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const fetchProfile = useCallback(async () => {
    if (!token) return;
    setIsLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/profile/`, {
        headers: { Authorization: `Token ${token}` },
      });
      setProfile(response.data);
    } catch (err) {
      setError('No se pudo cargar el perfil. Por favor, intente de nuevo.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, [token]);

  useEffect(() => {
    fetchProfile();
  }, [fetchProfile]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    if (!profile) return;
    const { name, value } = e.target;
    setProfile({ ...profile, [name]: value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!profile) return;
    setIsSaving(true);
    setError(null);
    setSuccess(null);
    try {
      await axios.put(`${API_BASE_URL}/profile/`, profile, {
        headers: { Authorization: `Token ${token}` },
      });
      setSuccess('¡Perfil actualizado con éxito!');
    } catch (err) {
      setError('Error al guardar el perfil. Por favor, verifique los datos.');
      console.error(err);
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) return <p>Cargando perfil...</p>;
  if (error && !profile) return <p className="text-red-500">{error}</p>;
  if (!profile) return <p>No se encontró un perfil de prestador asociado a esta cuenta.</p>;

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="p-4 bg-gray-100 rounded-md">
        <h3 className="font-bold">Información General</h3>
        <p>Categoría: <span className="font-semibold">{profile.categoria_nombre || 'No asignada'}</span></p>
        <p>Estado: {profile.aprobado ? <span className="font-semibold text-green-600">Aprobado</span> : <span className="font-semibold text-yellow-600">Pendiente de Aprobación</span>}</p>
      </div>

      {/* Campos del formulario */}
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        <div>
          <label htmlFor="nombre_negocio" className="block text-sm font-medium text-gray-700">Nombre del Negocio</label>
          <input type="text" name="nombre_negocio" id="nombre_negocio" value={profile.nombre_negocio} onChange={handleChange} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" />
        </div>
        <div>
          <label htmlFor="telefono" className="block text-sm font-medium text-gray-700">Teléfono</label>
          <input type="text" name="telefono" id="telefono" value={profile.telefono} onChange={handleChange} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" />
        </div>
        <div>
          <label htmlFor="email_contacto" className="block text-sm font-medium text-gray-700">Email de Contacto</label>
          <input type="email" name="email_contacto" id="email_contacto" value={profile.email_contacto} onChange={handleChange} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" />
        </div>
        <div>
          <label htmlFor="ubicacion_mapa" className="block text-sm font-medium text-gray-700">Ubicación (Dirección o Coordenadas)</label>
          <input type="text" name="ubicacion_mapa" id="ubicacion_mapa" value={profile.ubicacion_mapa} onChange={handleChange} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" />
        </div>
      </div>

      <div>
        <label htmlFor="descripcion" className="block text-sm font-medium text-gray-700">Descripción</label>
        <textarea name="descripcion" id="descripcion" value={profile.descripcion} onChange={handleChange} rows={4} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"></textarea>
      </div>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
        <div>
          <label htmlFor="red_social_facebook" className="block text-sm font-medium text-gray-700">Facebook (URL)</label>
          <input type="url" name="red_social_facebook" id="red_social_facebook" value={profile.red_social_facebook} onChange={handleChange} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" />
        </div>
        <div>
          <label htmlFor="red_social_instagram" className="block text-sm font-medium text-gray-700">Instagram (URL)</label>
          <input type="url" name="red_social_instagram" id="red_social_instagram" value={profile.red_social_instagram} onChange={handleChange} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" />
        </div>
        <div>
          <label htmlFor="red_social_whatsapp" className="block text-sm font-medium text-gray-700">WhatsApp</label>
          <input type="text" name="red_social_whatsapp" id="red_social_whatsapp" value={profile.red_social_whatsapp} onChange={handleChange} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" />
        </div>
      </div>

      <div>
        <label htmlFor="promociones_ofertas" className="block text-sm font-medium text-gray-700">Promociones y Ofertas</label>
        <textarea name="promociones_ofertas" id="promociones_ofertas" value={profile.promociones_ofertas} onChange={handleChange} rows={3} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"></textarea>
      </div>

      {/* Sección especial para hoteles */}
      {profile.categoria_nombre === 'Hotel' && (
        <div className="p-4 border-t border-gray-200">
          <h3 className="font-bold text-lg">Reporte de Ocupación (Solo Hoteles)</h3>
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 mt-4">
            <div>
              <label htmlFor="reporte_ocupacion_nacional" className="block text-sm font-medium text-gray-700">Ocupación Nacional</label>
              <input type="number" name="reporte_ocupacion_nacional" id="reporte_ocupacion_nacional" value={profile.reporte_ocupacion_nacional} onChange={handleChange} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" />
            </div>
            <div>
              <label htmlFor="reporte_ocupacion_internacional" className="block text-sm font-medium text-gray-700">Ocupación Internacional</label>
              <input type="number" name="reporte_ocupacion_internacional" id="reporte_ocupacion_internacional" value={profile.reporte_ocupacion_internacional} onChange={handleChange} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" />
            </div>
          </div>
        </div>
      )}

      {/* Botón de guardar y mensajes */}
      <div className="flex items-center justify-end space-x-4">
        {success && <p className="text-green-600">{success}</p>}
        {error && <p className="text-red-600">{error}</p>}
        <button type="submit" disabled={isSaving} className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-400">
          {isSaving ? 'Guardando...' : 'Guardar Cambios'}
        </button>
      </div>

      {/* Gestores de archivos */}
      <ImageGalleryManager initialImages={profile.galeria_imagenes} onUpdate={fetchProfile} />
      <DocumentManager initialDocuments={profile.documentos_legalizacion} onUpdate={fetchProfile} />
    </form>
  );
}