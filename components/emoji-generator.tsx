import { useState, useEffect } from 'react';
import { ImageCard } from './image-card';
import { Input } from './ui/input';
import { Button } from './ui/button';

interface Image {
  id: string;
  prompt: string;
  url: string;
  likes: number;
  created_at: string;
}

export function EmojiGenerator() {
  const [prompt, setPrompt] = useState('');
  const [images, setImages] = useState<Image[]>([]);
  const [loading, setLoading] = useState(false);
  const [fetchingImages] = useState(false);

  useEffect(() => {
    fetch('http://localhost:8000/images')
      .then(res => res.json())
      .then(data => setImages(data))
      .catch(err => console.error(err));
  }, []);

  const handleGenerate = async () => {
    if (!prompt.trim()) return;

    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/images/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: prompt.trim() }),
      });

      const newImage = await response.json();
      setImages(prev => [newImage, ...prev]);
      setPrompt('');
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleLike = async (imageId: string): Promise<number> => {
    const updatedImages = images.map(img => {
      if (img.id === imageId) {
        return { ...img };
      }
      return img;
    });
    setImages(updatedImages);
    return 0; // Return a number to satisfy the type
  };

  const handleDelete = async (imageId: string) => {
    try {
      await fetch(`http://localhost:8000/images/${imageId}`, {
        method: 'DELETE',
      });
      setImages(prev => prev.filter(image => image.id !== imageId));
    } catch (error) {
      console.error(error);
    }
  };

  const handleDownload = (url: string) => {
    window.open(url, '_blank');
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-xl mx-auto mb-8">
        <div className="flex gap-4">
          <Input
            placeholder="What would you like to generate?"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleGenerate()}
            disabled={loading}
          />
          <Button onClick={handleGenerate} disabled={loading}>
            {loading ? 'Generating...' : 'Generate'}
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {fetchingImages ? (
          <div className="col-span-full text-center py-8">Loading images...</div>
        ) : images.length === 0 ? (
          <div className="col-span-full text-center py-8">No images yet. Generate some!</div>
        ) : (
          images.map((image) => (
            <ImageCard
              key={image.id}
              {...image}
              onLike={handleLike}
              onDelete={() => handleDelete(image.id)}
              onDownload={handleDownload}
            />
          ))
        )}
      </div>
    </div>
  );
} 
