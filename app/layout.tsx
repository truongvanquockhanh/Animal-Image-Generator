"use client";

import { Inter } from "next/font/google";
import "./globals.css";
import { Toaster } from "sonner";
import { AuthProvider } from "@/contexts/auth-context";
import { GoogleOAuthProvider } from "@react-oauth/google";

const inter = Inter({
  subsets: ["latin"],
});

const googleClientId = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  if (!googleClientId) {
    console.error("Google Client ID is missing. Please set NEXT_PUBLIC_GOOGLE_CLIENT_ID in your environment variables.");
    // Optionally render an error message or fallback UI
    return (
      <html lang="en" suppressHydrationWarning>
        <body className={inter.className}>
          <div>Error: Google Client ID is not configured.</div>
        </body>
      </html>
    );
  }

  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <GoogleOAuthProvider clientId={googleClientId}>
          <AuthProvider>
            {children}
            <Toaster />
          </AuthProvider>
        </GoogleOAuthProvider>
      </body>
    </html>
  );
}
