import { useState } from 'react';
import { Heart, Download, Info, Trash2 } from 'lucide-react';

interface ImageCardProps {
  id: string;
  prompt: string;
  url: string;
  likes: number;
  onLike: (id: string) => Promise<number>;
  onDownload: (url: string) => void;
  onDelete: (id: string) => Promise<void>;
}

export function ImageCard({
  id,
  prompt,
  url,
  likes,
  onLike,
  onDownload,
  onDelete,
}: ImageCardProps) {
  const [isLiking, setIsLiking] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [currentLikes, setCurrentLikes] = useState(likes);
  const [isHovered, setIsHovered] = useState(false);
  const [showDescription, setShowDescription] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLike = async () => {
    if (isLiking) return;
    setIsLiking(true);
    setError(null);
    try {
      const newLikes = await onLike(id);
      setCurrentLikes(newLikes);
    } catch (err) {
      console.error('Error liking image:', err);
      setError('Failed to like image');
    } finally {
      setIsLiking(false);
    }
  };

  const handleDelete = async () => {
    if (isDeleting) return;
    if (!confirm('Are you sure you want to delete this image?')) return;
    
    setIsDeleting(true);
    setError(null);
    try {
      await onDelete(id);
    } catch (err) {
      console.error('Error deleting image:', err);
      setError('Failed to delete image');
      setIsDeleting(false);
    }
  };

  const capitalizeFirstLetter = (string: string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  };

  const generateDescription = (prompt: string) => {
    return `This is a beautiful ${prompt.toLowerCase()} image. The image showcases the unique characteristics and natural beauty of this amazing creature. It has received ${currentLikes} likes from our community.`;
  };

  if (isDeleting) {
    return null;
  }

  return (
    <div 
      className="bg-card rounded-lg shadow-lg overflow-hidden w-64 hover:shadow-xl transition-shadow duration-300"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="relative aspect-[3/4]">
        <img
          src={url}
          alt={prompt}
          className="w-full h-full object-cover"
        />
        {isHovered && (
          <div className="absolute inset-0 bg-black/40 flex items-center justify-center gap-4 transition-opacity duration-300">
            <button
              onClick={handleLike}
              className={`p-2 rounded-full backdrop-blur-sm transition-colors text-white ${
                isLiking ? 'bg-white/5 cursor-not-allowed' : 'bg-white/10 hover:bg-white/20'
              }`}
              disabled={isLiking}
            >
              <Heart className={`h-5 w-5 transition-colors ${isLiking ? 'text-gray-400' : error ? 'text-red-500' : ''}`} />
            </button>
            <button
              onClick={() => onDownload(url)}
              className="p-2 rounded-full bg-white/10 backdrop-blur-sm hover:bg-white/20 transition-colors text-white"
            >
              <Download className="h-5 w-5" />
            </button>
            <button
              onClick={handleDelete}
              className="p-2 rounded-full bg-red-500/60 backdrop-blur-sm hover:bg-red-500/80 transition-colors text-white"
            >
              <Trash2 className="h-5 w-5" />
            </button>
          </div>
        )}
      </div>
      <div className="p-3">
        <div className="flex items-center justify-between mb-2">
          <p className="text-sm font-medium line-clamp-2">{capitalizeFirstLetter(prompt)}</p>
          <button
            onClick={() => setShowDescription(!showDescription)}
            className="p-1 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            <Info className="h-4 w-4 text-gray-500" />
          </button>
        </div>
        {showDescription && (
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-2 mb-2">
            {generateDescription(prompt)}
          </p>
        )}
        <div className="flex items-center gap-1 text-sm text-gray-500">
          <Heart className={`h-4 w-4 ${error ? 'text-red-500' : ''}`} />
          <span>{currentLikes} likes</span>
          {error && <span className="text-xs text-red-500 ml-2">{error}</span>}
        </div>
      </div>
    </div>
  );
} 