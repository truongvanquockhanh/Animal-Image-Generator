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
      // Send the ID token (credential) to our backend
      const apiResponse = await fetch(`${API_BASE_URL}/auth/google`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        // Send the ID token received from Google
        body: JSON.stringify({ token: credentialResponse.credential }), 
      });

      const data: GoogleLoginResponse = await apiResponse.json();

      if (!apiResponse.ok) {
        throw new Error(data.detail || 'Google login failed');
      }

      // Login with the access_token from our backend
      login(data.access_token);
      toast.success('Successfully logged in with Google!');
      // Redirect or update UI
      window.location.href = '/'; 
    } catch (error) {
      console.error('Google login error:', error);
      toast.error(error instanceof Error ? error.message : 'Failed to login with Google');
    }
  };

  const handleGoogleError = () => {
    toast.error('Google login failed');
  };

  return (
    <div className="w-full">
      <GoogleLogin
        onSuccess={handleGoogleSuccess}
        onError={handleGoogleError}
        useOneTap // Optional: Enables One Tap sign-in experience
        width="100%" // Make the button full width
        theme="outline"
        shape="rectangular"
        logo_alignment="left"
      />
    </div>
  );
} 