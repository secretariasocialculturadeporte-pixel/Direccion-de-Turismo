"use client";

import React, { useState } from 'react';
import PrestadorManager from './PrestadorManager';
import MunicipioContentManager from './MunicipioContentManager';

type AdminTab = 'prestadores' | 'contenido';

export default function AdminDashboard() {
  const [activeTab, setActiveTab] = useState<AdminTab>('prestadores');

  const renderContent = () => {
    switch (activeTab) {
      case 'prestadores':
        return <PrestadorManager />;
      case 'contenido':
        return <MunicipioContentManager />;
      default:
        return null;
    }
  };

  const getTabClass = (tabName: AdminTab) => {
    return `px-4 py-2 font-semibold rounded-t-lg ${
      activeTab === tabName
        ? 'bg-white border-b-0 border-l border-t border-r'
        : 'bg-gray-100 hover:bg-gray-200'
    }`;
  };

  return (
    <div>
      <div className="border-b">
        <nav className="-mb-px flex space-x-2">
          <button
            onClick={() => setActiveTab('prestadores')}
            className={getTabClass('prestadores')}
          >
            Gestión de Prestadores
          </button>
          <button
            onClick={() => setActiveTab('contenido')}
            className={getTabClass('contenido')}
          >
            Gestión de Contenido
          </button>
        </nav>
      </div>
      <div className="mt-4">
        {renderContent()}
      </div>
    </div>
  );
}