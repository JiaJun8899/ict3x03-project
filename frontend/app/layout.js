'use client';
import { Providers } from "./providers";
import Nav from "./components/navbar";
import { usePathname } from 'next/navigation';
import axios from "axios";
import { API_HOST } from "@/app/utils/utils";
import { useEffect, useState } from "react";
export default function RootLayout({ children }) {  
  const pathname = usePathname();
  const [userRole, setUserRole] = useState("none");
  async function getRole() {
    try {
      const response = await axios.get(`${API_HOST}/test`, {
        withCredentials: true,
      });
      // console.log(response.data);
      setUserRole(response.data);
    } catch (error) {
      console.error("There was an fetching your profile", error);
    } 
  }

  useEffect(() => {
    getRole();    
  }, []);

  return (
    <html lang="en">
      <body>
        <Providers>
          {(userRole != "none")
           ?<Nav></Nav>:<></>}
          {children}
        </Providers>
      </body>
    </html>
  );
}
