import Link from 'next/link';

const socialLinks = [
  { name: 'Facebook', href: '#', icon: 'FB' }, // Placeholder icons
  { name: 'Instagram', href: '#', icon: 'IG' },
  { name: 'YouTube', href: '#', icon: 'YT' },
];

export default function Footer() {
  return (
    <footer className="bg-gray-800 text-white">
      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Contact Info */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Dirección de Turismo</h3>
            <p className="text-gray-400">
              Alcaldía Municipal de Puerto Gaitán <br />
              Puerto Gaitán, Meta, Colombia
            </p>
            <p className="text-gray-400">
              Email: <a href="mailto:turismo@puertogaitan.gov.co" className="hover:text-white">turismo@puertogaitan.gov.co</a>
            </p>
            <p className="text-gray-400">
              Teléfono: +57 123 456 7890
            </p>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Enlaces Rápidos</h3>
            <ul className="space-y-2">
              <li><Link href="/atractivos" className="text-gray-400 hover:text-white">Atractivos</Link></li>
              <li><Link href="/agenda-cultural" className="text-gray-400 hover:text-white">Agenda Cultural</Link></li>
              <li><Link href="/noticias" className="text-gray-400 hover:text-white">Noticias</Link></li>
              <li><Link href="/blog" className="text-gray-400 hover:text-white">Blog</Link></li>
              <li><Link href="/mapa" className="text-gray-400 hover:text-white">Mapa Interactivo</Link></li>
            </ul>
          </div>

          {/* Social Media */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Síguenos</h3>
            <div className="flex space-x-6">
              {socialLinks.map((item) => (
                <a key={item.name} href={item.href} className="text-gray-400 hover:text-white">
                  <span className="sr-only">{item.name}</span>
                  {/* Placeholder for actual SVG icons */}
                  <div className="h-6 w-6 border rounded-full flex items-center justify-center">
                    {item.icon}
                  </div>
                </a>
              ))}
            </div>
          </div>
        </div>

        <div className="mt-8 border-t border-gray-700 pt-8 text-center text-gray-400">
          <p>&copy; {new Date().getFullYear()} Municipio de Puerto Gaitán. Todos los derechos reservados.</p>
        </div>
      </div>
    </footer>
  );
}