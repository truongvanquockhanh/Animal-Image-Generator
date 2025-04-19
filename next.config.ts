import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Disable ESLint during build (you already have this setting)
  eslint: {
    ignoreDuringBuilds: true,
  },
  
  // Enable static export
  output: 'export',

  // Disable image optimization for static export
  images: {
    unoptimized: true,
  },
};

export default nextConfig;

