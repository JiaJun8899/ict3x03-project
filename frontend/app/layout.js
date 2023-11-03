"use client";
import { Providers } from "./providers";
import { Suspense } from "react";
import Nav from "./components/navbar";
import { getRole } from "@/app/utils/utils";
import { useEffect, useState } from "react";
export default function RootLayout({ children }) {
  const [userRole, setUserRole] = useState("none");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getRole(setUserRole, setLoading);
  }, []);
  return (
    <html lang="en">
      <body>
        <Providers>
          <Suspense fallback={<p>Loading ...</p>}>
            {loading ? (
              <p>Building nav...</p>
            ) : (
              (<Nav userRole={userRole}/>)                            
            )}
            {children}
          </Suspense>
        </Providers>
      </body>
    </html>
  );
}
