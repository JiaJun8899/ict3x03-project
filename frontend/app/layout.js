'use client';
import { Providers } from "./providers";
import Nav from "./components/navbar";
import { usePathname } from 'next/navigation';
export default function RootLayout({ children }) {  
  const pathname = usePathname();
  console.log(pathname)
  return (
    <html lang="en">
      <body>
        <Providers>
          {pathname!=="/login" ?<Nav></Nav>:<></>}
          {children}
        </Providers>
      </body>
    </html>
  );
}
