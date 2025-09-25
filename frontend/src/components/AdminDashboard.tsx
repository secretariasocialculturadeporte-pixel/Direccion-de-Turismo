"use client";
 import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import { useAuth } from "@/contexts/AuthContext";
import MunicipioContentManager from "./MunicipioContentManager";

const API_BASE_URL = "http://localhost:8000/api";

interface AdminPrestador {
  id: number;
  nombre_negocio: string;
  aprobado: boolean;
  fecha_creacion: string;
  categoria_nombre: string;
  usuario_email: string;
}

type AdminTab = "prestadores" | "contenido";

export default function AdminDashboard() {
  const { token } = useAuth();
  const [activeTab, setActiveTab] = useState<AdminTab>("prestadores");

  // --- Estado para Prestadores ---
  const [prestadores, setPrestadores] = useState<AdminPrestador[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<"all" | "approved" | "pending">(
    "pending"
  );

  const fetchPrestadores = useCallback(async () => {
    if (!token) return;
    setIsLoading(true);
    setError(null);

    let url = `${API_BASE_URL}/admin/prestadores/`;
    if (filter !== "all") {
      url += `?aprobado=${filter === "approved"}`;
    }

    try {
      const response = await axios.get(url, {
        headers: { Authorization: `Token ${token}` },
      });
      setPrestadores(response.data.results);
    } catch (err) {
      setError("No se pudo cargar la lista de prestadores.");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, [token, filter]);

  useEffect(() => {
    fetchPrestadores();
  }, [fetchPrestadores]);

  const handleApprove = async (id: number) => {
    if (!window.confirm("¿Está seguro de que desea aprobar a este prestador?"))
      return;

    try {
      await axios.patch(
        `${API_BASE_URL}/admin/prestadores/${id}/approve/`,
        {},
        {
          headers: { Authorization: `Token ${token}` },
        }
      );
      fetchPrestadores();
    } catch (err) {
      alert("Error al aprobar el prestador.");
      console.error(err);
    }
  };

  // --- Renderizado por tab ---
  const renderContent = () => {
    switch (activeTab) {
      case "prestadores":
        return (
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-2xl font-bold mb-4">
              Gestión de Prestadores de Servicios
            </h2>

            <div className="flex justify-end mb-4">
              <select
                value={filter}
                onChange={(e) =>
                  setFilter(e.target.value as "all" | "approved" | "pending")
                }
                className="px-4 py-2 border border-gray-300 rounded-md shadow-sm bg-white"
              >
                <option value="pending">Pendientes</option>
                <option value="approved">Aprobados</option>
                <option value="all">Todos</option>
              </select>
            </div>

            {isLoading ? (
              <p>Cargando prestadores...</p>
            ) : error ? (
              <p className="text-red-500">{error}</p>
            ) : (
              <div className="overflow-x-auto">
                <table className="min-w-full bg-white">
                  <thead className="bg-gray-100">
                    <tr>
                      <th className="py-2 px-4 text-left">Negocio</th>
                      <th className="py-2 px-4 text-left">Email Contacto</th>
                      <th className="py-2 px-4 text-left">Fecha Registro</th>
                      <th className="py-2 px-4 text-left">Estado</th>
                      <th className="py-2 px-4 text-left">Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {prestadores.map((p) => (
                      <tr key={p.id} className="border-b">
                        <td className="py-2 px-4">{p.nombre_negocio}</td>
                        <td className="py-2 px-4">{p.usuario_email}</td>
                        <td className="py-2 px-4">
                          {new Date(p.fecha_creacion).toLocaleDateString()}
                        </td>
                        <td className="py-2 px-4">
                          {p.aprobado ? (
                            <span className="px-2 py-1 text-xs font-semibold text-green-800 bg-green-200 rounded-full">
                              Aprobado
                            </span>
                          ) : (
                            <span className="px-2 py-1 text-xs font-semibold text-yellow-800 bg-yellow-200 rounded-full">
                              Pendiente
                            </span>
                          )}
                        </td>
                        <td className="py-2 px-4">
                          {!p.aprobado && (
                            <button
                              onClick={() => handleApprove(p.id)}
                              className="px-3 py-1 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700"
                            >
                              Aprobar
                            </button>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {prestadores.length === 0 && (
                  <p className="text-center py-4">
                    No hay prestadores en esta categoría.
                  </p>
                )}
              </div>
            )}
          </div>
        );
      case "contenido":
        return <MunicipioContentManager />;
      default:
        return null;
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Panel de Administración</h1>

      <div className="flex space-x-4 mb-6">
        <button
          onClick={() => setActiveTab("prestadores")}
          className={`px-4 py-2 rounded-md ${
            activeTab === "prestadores"
              ? "bg-blue-600 text-white"
              : "bg-gray-200 text-gray-700"
          }`}
        >
          Prestadores
        </button>
        <button
          onClick={() => setActiveTab("contenido")}
          className={`px-4 py-2 rounded-md ${
            activeTab === "contenido"
              ? "bg-blue-600 text-white"
              : "bg-gray-200 text-gray-700"
          }`}
        >
          Contenido Municipio
        </button>
      </div>

      {renderContent()}
    </div>
  );
}
        return <MunicipioContentManager />;
      default:
        return null;
    }
  };

  const getTabClass = (tabName: AdminTab) => {
    return `px-4 py-2 font-semibold rounded-t-lg ${
      activeTab === tabName
   ? "bg-white border-b-0 border-l border-t border-r"
        : "bg-gray-100 hover:bg-gray-200"
    }`;
  };

  return (
    <div>
      <div className="border-b">
        <nav className="-mb-px flex space-x-2">
          <button
  onClick={() => setActiveTab("prestadores")}
            className={getTabClass("prestadores")}
          >
            Gestión de Prestadores
          </button>
          <button
                  onClick={() => setActiveTab("contenido")}
            className={getTabClass("contenido")}
          >
            Gestión de Contenido
          </button>
        </nav>
      </div>
      <div className="mt-4">
  {renderContent()}
</div>
       
  );
}
 
