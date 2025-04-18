"use client";

import { useAuth } from "@/contexts/auth-context";
import { GoogleLogin, CredentialResponse } from "@react-oauth/google";
import { toast } from "sonner";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

interface GoogleLoginResponse {
  access_token: string;
  token_type: string;
  detail?: string;
}

export function GoogleLoginButton() {
  const { login } = useAuth();

  const handleGoogleSuccess = async (credentialResponse: CredentialResponse) => {
    if (!credentialResponse.credential) {
      toast.error('Google login failed: No credential received');
      return;
    }

    try {
      // Send the ID token to our backend
      const apiResponse = await fetch(`${API_BASE_URL}/auth/google`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: credentialResponse.credential }),
      });

      if (!apiResponse.ok) {
        const errorData = await apiResponse.json();
        throw new Error(errorData.detail || 'Google login failed');
      }

      const data: GoogleLoginResponse = await apiResponse.json();
      login(data.access_token);
      toast.success('Successfully logged in with Google!');
      window.location.href = '/';
    } catch (error) {
      console.error('Google login error:', error);
      toast.error(error instanceof Error ? error.message : 'Failed to login with Google');
    }
  };

  return (
    <div className="w-full flex justify-center">
      <GoogleLogin
        onSuccess={handleGoogleSuccess}
        onError={() => {
          toast.error('Google login failed');
        }}
        theme="outline"
        size="large"
        width="300"
        text="continue_with"
        shape="rectangular"
      />
    </div>
  );
} 