import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function POST(request: Request) {
  try {
    const { imageId, action } = await request.json();

    if (!imageId || !action) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      );
    }

    // Find the image
    const image = await prisma.image.findUnique({
      where: { id: imageId },
    });

    if (!image) {
      return NextResponse.json(
        { error: 'Image not found' },
        { status: 404 }
      );
    }

    // Update the likes count
    const updatedImage = await prisma.image.update({
      where: { id: imageId },
      data: {
        likes: action === 'like' ? image.likes + 1 : Math.max(0, image.likes - 1),
      },
    });

    return NextResponse.json({
      success: true,
      likes: updatedImage.likes,
    });
  } catch (error) {
    console.error('Error handling like:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
} 