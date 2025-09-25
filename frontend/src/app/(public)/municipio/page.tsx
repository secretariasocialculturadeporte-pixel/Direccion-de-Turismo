import React from 'react';

// Componente para una sección con título
const InfoSection = ({ title, children }: { title: string, children: React.ReactNode }) => (
  <section className="mb-12">
    <h2 className="text-3xl font-bold text-gray-800 border-b-2 border-blue-500 pb-2 mb-6">{title}</h2>
    <div className="prose prose-lg max-w-none text-gray-700">
      {children}
    </div>
  </section>
);

// Componente para un contacto de emergencia o entidad
const ContactCard = ({ title, address, phone }: { title: string, address?: string, phone?: string }) => (
    <div className="bg-gray-100 p-4 rounded-lg shadow-sm">
        <h4 className="font-bold text-lg text-gray-800">{title}</h4>
        {address && <p className="text-sm text-gray-600">{address}</p>}
        {phone && <p className="text-sm font-semibold text-blue-600">{phone}</p>}
    </div>
);

export default function MunicipioPage() {
  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <header className="text-center mb-12">
        <h1 className="text-5xl font-extrabold text-blue-800 tracking-tight">Conoce Puerto Gaitán</h1>
        <p className="mt-4 text-xl text-gray-600">El Paraíso Natural de Colombia</p>
      </header>

      <main>
        <InfoSection title="Datos Generales del Municipio">
          <p>
            Puerto Gaitán es uno de los municipios más importantes del departamento del Meta, tanto por su extensión territorial como por su riqueza cultural y natural.
            Con una población de 46.127 habitantes, los portogaitenses son un ejemplo de la diversidad de los Llanos Orientales, con una fuerte presencia de comunidades indígenas. De hecho, el 31,67% de la población pertenece a las etnias Sikuani, Saliva y Piapoco, quienes habitan en nueve resguardos indígenas distribuidos a lo largo del municipio. Estas comunidades han preservado sus costumbres, lengua y modos de vida tradicionales, lo que añade un valor cultural significativo a Puerto Gaitán.
          </p>
          <p>
            Ubicado a una altura de 149 metros sobre el nivel del mar, el municipio se extiende sobre una vasta área que abarca importantes ríos como el Meta, Manacacías y Yucao. Esto le otorga un papel fundamental en la economía regional, especialmente en la industria petrolera, una de las actividades más prominentes en la zona. No obstante, Puerto Gaitán también destaca por sus iniciativas de turismo sostenible, con un fuerte enfoque en el ecoturismo y la promoción de las tradiciones indígenas y campesinas.
          </p>
        </InfoSection>

        <InfoSection title="Ubicación y Clima">
          <p>
            Puerto Gaitán está ubicado en los Llanos Orientales de Colombia, al oriente del departamento del Meta, siendo un punto clave de la región llanera por su importancia económica y cultural.
          </p>
          <ul className="list-disc pl-5 space-y-2">
            <li>Se encuentra a <strong>281 kilómetros de Bogotá</strong>, lo que equivale a aproximadamente 6 horas en automóvil, dependiendo del tráfico y las condiciones climáticas.</li>
            <li>Desde <strong>Villavicencio</strong>, la capital departamental del Meta, la distancia es menor, con <strong>189 kilómetros</strong>, lo que representa un viaje de 4 horas aproximadamente.</li>
          </ul>
          <p>
            Ambas rutas ofrecen vistas de la geografía llanera, con llanuras extensas, ríos y montañas en el horizonte, haciendo del viaje una experiencia visual única.
          </p>
          <p>
            El clima en Puerto Gaitán es mayormente cálido durante todo el año. Con una temperatura promedio de <strong>32°C</strong>, se caracteriza por ser ligeramente húmedo debido a su proximidad con varios ríos importantes de la región. La temporada de lluvias, que va de abril a octubre, contrasta con los meses secos de enero a marzo, cuando las condiciones son ideales para disfrutar de las playas de río y actividades al aire libre. Durante el año, la precipitación promedio es de 2.300 mm, lo que favorece la biodiversidad del área y permite una vegetación verde y frondosa en la región. Esta combinación entre clima cálido y fresco, dependiendo de la temporada, hace de Puerto Gaitán un destino turístico atractivo en cualquier época del año.
          </p>
        </InfoSection>

        <InfoSection title="¿Dónde Dormir?">
            <p>Puerto Gaitán ofrece una amplia gama de opciones de alojamiento que se adaptan a todo tipo de viajeros, desde aquellos que buscan confort, hasta quienes prefieren una experiencia más cercana a la naturaleza.</p>
            <ul className="list-disc pl-5 space-y-4">
                <li><strong>Hotel Luxor Plaza:</strong> Una excelente opción en el casco urbano, moderno y a solo 500 metros del malecón.</li>
                <li><strong>Hotel Puerta al Llano:</strong> Conocido por su atención personalizada y su historia de más de 30 años. Cuenta con restaurante, salones de conferencias y una terraza 360°.</li>
                <li><strong>Best Western Puerto Gaitán:</strong> Para quienes buscan exclusividad, es el único hotel de cadena en la región. Ubicado en las afueras, ofrece gimnasio, piscina y business center.</li>
                <li><strong>Hotel Guarataro Campestre:</strong> Ideal para amantes de la naturaleza. A solo 10 minutos del casco urbano, ofrece 12 cabañas rodeadas de zonas verdes y actividades como senderismo y avistamiento de aves.</li>
            </ul>
        </InfoSection>

        <InfoSection title="¿Cómo Llegar?">
            <h3 className="text-2xl font-semibold mb-4">En Carro</h3>
            <ol className="list-decimal pl-5 space-y-3">
                <li><strong>Salida de Bogotá:</strong> Inicia el viaje por la Autopista Sur o la Carretera 40 hacia el sur. Conéctate con la Autopista al Llano (Ruta 40).</li>
                <li><strong>Carretera Bogotá – Villavicencio:</strong> Sigue por la Autopista al Llano. El recorrido dura aproximadamente 2.5 a 3 horas (86 km).</li>
                <li><strong>De Villavicencio a Puerto Gaitán:</strong> Continúa por la Ruta 40 hasta el cruce con la Ruta 65 (Troncal del Llano). Sigue hacia el oriente, pasando por Puerto López. Desde allí, son aproximadamente 113 km hasta Puerto Gaitán.</li>
                <li><strong>Llegada a Puerto Gaitán:</strong> Ingresarás por la Carrera 13. Sigue las señales hacia el centro, el Malecón o el Parque Principal.</li>
            </ol>

            <h3 className="text-2xl font-semibold mt-8 mb-4">En Bus</h3>
            <p>Puerto Gaitán no cuenta con una terminal formal. Deberás hacer escala en Villavicencio.</p>
            <ul className="list-disc pl-5 space-y-2">
                <li><strong>Flota La Macarena:</strong> Bogotá-Villavicencio (~$40,000 COP), Villavicencio-Puerto Gaitán (~$47,000 COP).</li>
                <li><strong>TaxMeta:</strong> Villavicencio-Puerto Gaitán (~$45,000 COP).</li>
                <li><strong>Arimena:</strong> Villavicencio-Puerto Gaitán (~$45,000 COP).</li>
            </ul>

            <h3 className="text-2xl font-semibold mt-8 mb-4">En Avión</h3>
            <p>La forma más rápida es volar al Aeropuerto La Vanguardia en Villavicencio (VVC). Aerolíneas como SATENA, Avianca y Clic Air operan esta ruta desde Bogotá (1 hora aprox.). Desde Villavicencio, el viaje continúa por carretera (3-4 horas).</p>
        </InfoSection>

        <InfoSection title="Información Importante">
            <p>Antes de iniciar tu viaje, ten a mano estos contactos útiles:</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
                <ContactCard title="Policía Nacional" phone="+57 320 730 7009" />
                <ContactCard title="Bomberos" address="Calle 18 #9A-100" phone="+57 318 618 0086" />
                <ContactCard title="Hospital Local" address="Calle 10 #10-60" phone="+57 321 404 2836" />
            </div>

            <h3 className="text-2xl font-semibold mt-8 mb-4">Entidades Financieras</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
                <ContactCard title="Banco de Bogotá" address="Cra. 13 #7 – 50" />
                <ContactCard title="BBVA" address="Cra. 13 #9-18" phone="86460358" />
                <ContactCard title="Bancolombia" address="Cl. 10 #5-39" />
            </div>
            <p className="text-sm text-gray-500 mt-4">El horario de atención de los bancos es generalmente de lunes a viernes, de 8:00 a.m. a 11:30 a.m. y de 2:00 p.m. a 4:30 p.m.</p>
        </InfoSection>

      </main>
    </div>
  );
}