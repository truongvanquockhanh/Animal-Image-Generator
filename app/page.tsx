"use client";

import { useState, useEffect } from 'react';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useAuth } from '@/contexts/auth-context';
import { UserCircle, Sparkles } from 'lucide-react';
import { Sidebar } from '@/components/ui/sidebar';
import { API_BASE_URL } from '@/lib/constants';
import { ImageCard } from '@/components/image-card';
import { useRouter } from 'next/navigation';
import { v4 as uuidv4 } from 'uuid';

interface Image {
  id: string;
  prompt: string;
  url: string;
  likes: number;
  created_at: string;
}

interface Suggestion {
  animal: string;
  imageUrl: string | null;
}

const AVAILABLE_ANIMALS = [
  "dog", "cat", "lion", "tiger", "elephant", "penguin", "panda", 
  "koala", "giraffe", "dolphin", "fox", "wolf", "rabbit", "cow", 
  "horse", "sheep", "goat", "pig", "chicken", "duck", "turkey", 
  "peacock", "parrot", "pigeon", "sparrow", "rooster", "hen", "cock", "fish", 
  "shark", "whale", "dolphin", "octopus", "crab", "lobster", "snail", "butterfly", 
  "bee", "ant", "spider", "snake", "lizard", "turtle", "tortoise", "bird", 
  "owl", "eagle", "hawk", "falcon" 
]

export default function EmojiGenerator() {
  const router = useRouter();
  const { token, logout, isAuthenticated, username } = useAuth();
  const [prompt, setPrompt] = useState('');
  const [images, setImages] = useState<Image[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [suggestion, setSuggestion] = useState<Suggestion | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    fetchImages();
  }, [isAuthenticated, token]);

  const fetchImages = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/images`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (!response.ok) throw new Error('Failed to fetch images');
      const data = await response.json();
      setImages(data);
    } catch (error) {
      console.error('Error fetching images:', error);
    }
  };

  const generateSuggestion = () => {
    const randomIndex = Math.floor(Math.random() * AVAILABLE_ANIMALS.length);
    return AVAILABLE_ANIMALS[randomIndex];
  };

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    
    const normalizedPrompt = prompt.trim().toLowerCase();
    if (!AVAILABLE_ANIMALS.includes(normalizedPrompt)) {
      const suggestedAnimal = generateSuggestion();
      setIsLoading(true);
      try {
        // Generate a preview image for the suggestion
        const response = await fetch(`${API_BASE_URL}/images/generate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ prompt: suggestedAnimal })
        });

        if (!response.ok) {
          throw new Error('Failed to generate suggestion image');
        }

        const data = await response.json();
        setSuggestion({
          animal: suggestedAnimal,
          imageUrl: data.url
        });
      } catch (error) {
        console.error('Error generating suggestion:', error);
        setSuggestion({
          animal: suggestedAnimal,
          imageUrl: null
        });
      } finally {
        setIsLoading(false);
      }
      return;
    }

    setIsLoading(true);
    try {
      // Generate image
      const response = await fetch(`${API_BASE_URL}/images/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ prompt })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to generate image');
      }

      const data = await response.json();
      
      // Save the image
      const saveResponse = await fetch(`${API_BASE_URL}/images`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          id: data.id,
          prompt: data.prompt,
          url: data.url,
          likes: 0,
          created_at: new Date().toISOString(),
          is_suggested: false,
          suggested_animal: null,
          original_input: prompt
        })
      });

      if (!saveResponse.ok) {
        const errorData = await saveResponse.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to save image');
      }

      await fetchImages();
      setPrompt('');
      setSuggestion(null);
    } catch (error) {
      console.error('Error:', error);
      alert(error instanceof Error ? error.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAcceptSuggestion = async () => {
    if (suggestion && suggestion.imageUrl) {
      setIsLoading(true);
      try {
        // Save using the exact schema that FastAPI expects
        const saveResponse = await fetch(`${API_BASE_URL}/images`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            id: uuidv4(), // Using uuid v4 instead of crypto.randomUUID
            prompt: suggestion.animal,
            url: suggestion.imageUrl,
            likes: 0,
            created_at: new Date().toISOString(),
            is_suggested: true,
            suggested_animal: suggestion.animal,
            original_input: prompt
          })
        });

        if (!saveResponse.ok) {
          const errorData = await saveResponse.json().catch(() => ({}));
          throw new Error(errorData.detail || 'Failed to save image');
        }

        await fetchImages();
        setPrompt('');
        setSuggestion(null);
      } catch (error) {
        console.error('Error:', error);
        alert(error instanceof Error ? error.message : 'An error occurred');
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleRejectSuggestion = () => {
    setSuggestion(null);
    setPrompt('');
  };

  const handleLike = async (imageId: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/images/${imageId}/like`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to like image');
      }

      const data = await response.json();
      return data.likes;
    } catch (error) {
      console.error('Error liking image:', error);
      throw error;
    }
  };

  const handleDownload = (url: string) => {
    window.open(url, '_blank');
  };

  const handleDelete = async (imageId: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/images/${imageId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to delete image');
      }

      await fetchImages();
    } catch (error) {
      console.error('Error deleting image:', error);
      alert(error instanceof Error ? error.message : 'Failed to delete image');
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-8">
      <div className="flex justify-between items-center mb-8 py-4 border-b">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-gradient-to-br from-violet-500 via-purple-500 to-indigo-500">
              <Sparkles className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-violet-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
                Animal Image Generator
              </h1>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                Create unique animal images with AI
              </p>
            </div>
          </div>

          {/* Welcome Message */}
          {username && (
            <div className="border-l border-gray-200 dark:border-gray-700 pl-6">
              <p className="text-xl font-medium text-gray-700 dark:text-gray-300">
                Welcome, <span className="text-violet-600 dark:text-violet-400">{username}</span>!
              </p>
            </div>
          )}
        </div>

        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setIsSidebarOpen(false)}
            className="hover:bg-gray-100 dark:hover:bg-gray-800"
          >
            <UserCircle className="h-6 w-6" />
          </Button>
          <Button 
            onClick={logout}
            className="bg-gradient-to-r from-red-500 to-pink-500 hover:from-red-600 hover:to-pink-600 text-white font-medium px-6"
          >
            Logout
          </Button>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        <div className="flex gap-2 max-w-3xl mx-auto w-full">
          <Input
            type="text"
            placeholder="Enter an animal name..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                if (suggestion) {
                  handleAcceptSuggestion();
                } else if (!isLoading) {
                  handleGenerate();
                }
              }
            }}
            className="flex-grow h-12 text-lg rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 shadow-sm"
          />
          <Button 
            onClick={handleGenerate} 
            disabled={isLoading}
            className="h-12 px-8 rounded-xl bg-black hover:bg-gray-800 text-white font-medium text-lg transition-colors"
          >
            {isLoading ? 'Generating...' : 'Generate'}
          </Button>
        </div>

        {suggestion && (
          <div className="max-w-3xl mx-auto w-full bg-gray-50 dark:bg-gray-800/50 backdrop-blur-sm p-6 rounded-2xl shadow-sm">
            <p className="text-gray-600 dark:text-gray-300 text-lg mb-6">
              No animal matches your search. How about a cute {suggestion.animal} instead?
            </p>
            {suggestion.imageUrl && (
              <div className="mb-6 flex justify-center">
                <img 
                  src={suggestion.imageUrl} 
                  alt={suggestion.animal}
                  className="w-64 h-64 object-contain bg-white rounded-xl shadow-md"
                />
              </div>
            )}
            <div className="flex justify-center gap-4">
              <Button 
                onClick={handleAcceptSuggestion} 
                className="bg-black hover:bg-gray-800 text-white px-6 py-2 rounded-xl font-medium transition-colors"
              >
                Use this animal
              </Button>
              <Button 
                onClick={handleRejectSuggestion} 
                variant="outline"
                className="bg-white hover:bg-gray-50 text-gray-800 px-6 py-2 rounded-xl font-medium border border-gray-200 transition-colors"
              >
                No, thanks
              </Button>
            </div>
          </div>
        )}

        <div className="grid grid-cols-4 gap-12 justify-items-center mt-8">
          {images.map((image) => (
            <ImageCard
              key={image.id}
              id={image.id}
              prompt={image.prompt}
              url={image.url}
              likes={image.likes}
              onLike={handleLike}
              onDownload={handleDownload}
              onDelete={handleDelete}
            />
          ))}
        </div>
      </div>

      <Sidebar
        isOpen={isSidebarOpen}
        onToggle={() => setIsSidebarOpen(false)}
      />

      {!isSidebarOpen && (
        <Button
          onClick={() => setIsSidebarOpen(true)}
          className="fixed bottom-6 right-6 bg-gradient-to-r from-violet-500 to-purple-500 hover:from-violet-600 hover:to-purple-600 text-white shadow-lg"
        >
          <UserCircle className="w-5 h-5 mr-2" />
          Show Profile
        </Button>
      )}
    </div>
  );
}
