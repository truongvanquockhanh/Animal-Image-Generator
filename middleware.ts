import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// This function can be marked `async` if using `await` inside
export function middleware(request: NextRequest) {
  // console.log("middleware is running");
  
  // // Check both cookie and authorization header
  // const authToken = request.cookies.get('auth_token')?.value || 
  //                  request.headers.get('authorization')?.split(' ')[1];
                   
  // console.log('Auth token in middleware:', authToken);
  
  // const isLoginPage = request.nextUrl.pathname === '/login';
  // const isSignupPage = request.nextUrl.pathname === '/signup';
  // const isPublicPath = isLoginPage || isSignupPage;

  // // If has token but trying to access login/signup
  // if (authToken && isPublicPath) {
  //   console.log('Has token, redirecting to home');
  //   return NextResponse.redirect(new URL('/', request.url));
  // }

  // // If no token and trying to access protected route
  // if (!authToken && !isPublicPath) {
  //   console.log('No token, redirecting to login');
  //   return NextResponse.redirect(new URL('/login', request.url));
  // }

  // return NextResponse.next();
}

// See "Matching Paths" below to learn more
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
} 