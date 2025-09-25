import axios from 'axios';

// Define la URL base de tu API de Django
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// --- Tipos de Datos ---

export interface Categoria {
  id: number;
  nombre: string;
  slug: string;
}

export interface ImagenGaleria {
  id: number;
  imagen: string;
  alt_text: string;
}

export interface PrestadorPublico {
  id: number;
  nombre_negocio: string;
  categoria_nombre: string;
  imagen_principal: string | null;
}

export interface PrestadorPublicoDetalle {
  id: number;
  nombre_negocio: string;
  descripcion: string;
  telefono: string;
  email_contacto: string;
  red_social_facebook: string;
  red_social_instagram: string;
  red_social_whatsapp: string;
  ubicacion_mapa: string;
  promociones_ofertas: string;
  categoria: Categoria;
  galeria_imagenes: ImagenGaleria[];
}


// --- Funciones de la API ---

/**
 * Obtiene la lista de todas las categorías de prestadores.
 */
export const getCategorias = async (): Promise<Categoria[]> => {
  const response = await apiClient.get('/prestadores/categorias/');
  return response.data;
};

/**
 * Obtiene la lista de prestadores de servicios públicos.
 * @param categoriaSlug - (Opcional) El slug de la categoría para filtrar los resultados.
 * @param searchTerm - (Opcional) El término de búsqueda para filtrar por nombre o descripción.
 */
export const getPrestadores = async (categoriaSlug?: string, searchTerm?: string): Promise<PrestadorPublico[]> => {
  const params = new URLSearchParams();
  if (categoriaSlug) {
    params.append('categoria', categoriaSlug);
  }
  if (searchTerm) {
    params.append('search', searchTerm);
  }

  const response = await apiClient.get('/prestadores/', { params });
  return response.data;
};

/**
 * Obtiene el detalle de un prestador de servicio por su ID.
 * @param id - El ID del prestador.
 */
export const getPrestadorById = async (id: number): Promise<PrestadorPublicoDetalle> => {
  const response = await apiClient.get(`/prestadores/${id}/`);
  return response.data;
};