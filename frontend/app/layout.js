"use client";
import { Providers } from "./providers";
import { Suspense } from "react";
import Nav from "./components/navbar";
import { usePathname } from "next/navigation";
import axios from "axios";
import { API_HOST, getRole } from "@/app/utils/utils";
import { useEffect, useState } from "react";
export default function RootLayout({ children }) {
  const pathname = usePathname();
  const [userRole, setUserRole] = useState("none");
  const [loading, setLoading] = useState(true);
  // async function getRole() {
  //   try {
  //     const response = await axios.get(`${API_HOST}/test`, {
  //       withCredentials: true,
  //     });
  //     // console.log(response.data);
  //     setUserRole(response.data);
  //   } catch (error) {
  //     console.error("There was an fetching your profile", error);
  //   }
  // }

  useEffect(() => {
    getRole(setUserRole, setLoading);
  }, []);
  console.log(userRole)
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
