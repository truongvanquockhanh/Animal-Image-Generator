"use client";

import { useState, useEffect } from 'react';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useAuth } from '@/contexts/auth-context';
import { UserCircle } from 'lucide-react';
import { Sidebar } from '@/components/ui/sidebar';
import { API_BASE_URL } from '@/lib/constants';
import { ImageCard } from '@/components/image-card';

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
  const [prompt, setPrompt] = useState('');
  const [images, setImages] = useState<Image[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [suggestion, setSuggestion] = useState<Suggestion | null>(null);
  const { token, logout } = useAuth();

  useEffect(() => {
    fetchImages();
  }, []);

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
    if (suggestion) {
      setPrompt(suggestion.animal);
      handleGenerate();
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
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Animal Image Generator</h1>
        <div className="flex gap-2">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setIsSidebarOpen(true)}
          >
            <UserCircle className="h-6 w-6" />
          </Button>
          <Button onClick={logout}>Logout</Button>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        <div className="flex gap-2">
          <Input
            type="text"
            placeholder="Enter an animal name..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            className="flex-grow"
          />
          <Button onClick={handleGenerate} disabled={isLoading}>
            {isLoading ? 'Generating...' : 'Generate'}
          </Button>
        </div>

        {suggestion && (
          <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg">
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              No animal matches your search. How about a cute {suggestion.animal} instead?
            </p>
            {suggestion.imageUrl && (
              <div className="mb-4">
                <img 
                  src={suggestion.imageUrl} 
                  alt={suggestion.animal}
                  className="w-48 h-48 object-cover rounded-lg mx-auto"
                />
              </div>
            )}
            <div className="flex justify-center gap-4">
              <Button onClick={handleAcceptSuggestion} variant="default">
                Use this animal
              </Button>
              <Button onClick={handleRejectSuggestion} variant="outline">
                No, thanks
              </Button>
            </div>
          </div>
        )}

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 justify-items-center">
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
        onToggle={() => setIsSidebarOpen(!isSidebarOpen)}
      />
    </div>
  );
}
