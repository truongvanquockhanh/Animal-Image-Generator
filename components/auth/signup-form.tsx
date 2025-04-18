"use client";

import { useState, useEffect } from "react";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/contexts/auth-context";
import { toast } from "sonner";
import { API_BASE_URL } from "@/lib/constants";

interface SignupResponse {
  id: string;
  username: string;
  token: string;
}

export function SignupForm() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isCheckingUsername, setIsCheckingUsername] = useState(false);
  const [usernameError, setUsernameError] = useState<string | null>(null);
  const { login } = useAuth();

  // Debounce username check
  useEffect(() => {
    const checkUsername = async () => {
      if (!username || username.length < 3) {
        setUsernameError(username ? "Username must be at least 3 characters" : null);
        return;
      }

      setIsCheckingUsername(true);
      try {
        const response = await fetch(`${API_BASE_URL}/auth/check-username?username=${encodeURIComponent(username)}`);
        if (response.status === 409) {
          setUsernameError("Username is already taken");
        } else if (response.ok) {
          setUsernameError(null);
        }
      } catch (error) {
        console.error("Error checking username:", error);
      } finally {
        setIsCheckingUsername(false);
      }
    };

    const timeoutId = setTimeout(checkUsername, 500); // Debounce for 500ms
    return () => clearTimeout(timeoutId);
  }, [username]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validation checks
    if (password !== confirmPassword) {
      toast.error("Passwords do not match");
      return;
    }

    if (password.length < 6) {
      toast.error("Password must be at least 6 characters");
      return;
    }

    if (usernameError) {
      toast.error("Please fix username errors before submitting");
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/auth/signup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          password,
        }),
      });

      const data: SignupResponse = await response.json();

      if (!response.ok) {
        throw new Error(response.status === 409 ? "Username is already taken" : "Signup failed");
      }

      login(data.token);
      toast.success("Successfully signed up!");

    } catch (error) {
      console.error("Signup error:", error);
      toast.error(error instanceof Error ? error.message : "Failed to sign up");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md p-6 space-y-6 bg-white shadow-lg rounded-lg">
      <div className="space-y-2 text-center">
        <h1 className="text-3xl font-bold">Create an account</h1>
        <p className="text-gray-500">Enter your details to create your account</p>
      </div>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <label htmlFor="username" className="text-sm font-medium">
            Username
          </label>
          <div className="relative">
            <Input
              id="username"
              placeholder="Enter your username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              minLength={3}
              className={usernameError ? "border-red-500" : ""}
              disabled={isLoading}
            />
            {isCheckingUsername && (
              <span className="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-gray-500">
                Checking...
              </span>
            )}
          </div>
          {usernameError && (
            <p className="text-sm text-red-500 mt-1">{usernameError}</p>
          )}
        </div>
        <div className="space-y-2">
          <label htmlFor="password" className="text-sm font-medium">
            Password
          </label>
          <Input
            id="password"
            placeholder="Enter your password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={6}
            disabled={isLoading}
          />
          <p className="text-xs text-gray-500">Must be at least 6 characters</p>
        </div>
        <div className="space-y-2">
          <label htmlFor="confirmPassword" className="text-sm font-medium">
            Confirm Password
          </label>
          <Input
            id="confirmPassword"
            placeholder="Confirm your password"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
            disabled={isLoading}
          />
        </div>
        <Button
          type="submit"
          className="w-full"
          disabled={isLoading || isCheckingUsername || Boolean(usernameError)}
        >
          {isLoading ? "Signing up..." : "Sign up"}
        </Button>
      </form>
      <div className="text-center text-sm">
        <a href="/login" className="text-blue-600 hover:underline">
          Already have an account? Log in
        </a>
      </div>
    </Card>
  );
} 