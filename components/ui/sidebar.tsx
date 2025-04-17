import { FC } from 'react';
import { ChevronDown, Github, Facebook } from 'lucide-react';
import { Button } from './button';

interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
}

export const Sidebar: FC<SidebarProps> = ({ isOpen, onToggle }) => {
  return (
    <div
      className={`fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-800 shadow-lg transform transition-transform duration-300 ease-in-out ${
        isOpen ? 'translate-y-0' : 'translate-y-full'
      }`}
      style={{ zIndex: 1000 }}
    >
      <div className="relative p-6">
        <Button
          variant="ghost"
          size="icon"
          onClick={onToggle}
          className="absolute top-2 right-2 p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700"
        >
          <ChevronDown className="w-6 h-6" />
          <span className="sr-only">Hide Profile</span>
        </Button>

        <div className="max-w-4xl mx-auto">
          <div className="flex items-center gap-4 mb-6">
            <div className="w-16 h-16 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center">
              <span className="text-2xl font-bold text-white">KT</span>
            </div>
            <div>
              <h2 className="text-xl font-bold">Khanh Truong</h2>
              <p className="text-gray-600 dark:text-gray-400">Full Stack Developer</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Contact Information</h3>
              <div className="space-y-2">
                <a
                  href="mailto:truongvanquockhanh@gmail.com"
                  className="flex items-center gap-2 text-blue-600 dark:text-blue-400 hover:underline"
                >
                  📧 truongvanquockhanh@gmail.com
                </a>
                <a
                  href="tel:+84901704689"
                  className="flex items-center gap-2 text-blue-600 dark:text-blue-400 hover:underline"
                >
                  📱 +84 901704689
                </a>
                <div className="flex items-center gap-4 pt-2">
                  <a
                    href="https://github.com/dragonknight"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400"
                  >
                    <Github className="w-5 h-5" />
                    <span>GitHub</span>
                  </a>
                  <a
                    href="https://facebook.com/truongvanquockhanh"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400"
                  >
                    <Facebook className="w-5 h-5" />
                    <span>Facebook</span>
                  </a>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="text-lg font-semibold">About</h3>
              <p className="text-gray-600 dark:text-gray-400">
                Full Stack Developer with expertise in Next.js, React, and FastAPI. 
                Passionate about building beautiful and functional web applications.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}; 