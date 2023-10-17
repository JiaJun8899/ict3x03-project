import { Providers } from "./providers";
import Nav from "./components/navbar";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <Nav></Nav>
          {children}
        </Providers>
      </body>
    </html>
  );
}
