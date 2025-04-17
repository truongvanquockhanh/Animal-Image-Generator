export interface Image {
  id: string;
  prompt: string;
  url: string;
  likes: number;
  created_at: string;
}

export interface PreviewImage {
  id: string;
  prompt: string;
  url: string;
  originalInput?: string;
  is_suggested?: boolean;
} 