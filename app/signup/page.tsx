"use client";

import { SignupForm } from "@/components/auth/signup-form";
import { useAuth } from "@/contexts/auth-context";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function SignupPage() {
  const { isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated) {
      router.push("/"); // Redirect if already logged in
    }
  }, [isAuthenticated, router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <SignupForm />
    </div>
  );
} 