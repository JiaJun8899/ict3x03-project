// app/page.tsx
"use client";
import { Link } from "@chakra-ui/next-js";
import { Box } from "@chakra-ui/react";
import Nav from "./components/navbar"

export default function Page() {
  return (
    <>
    {/* <Nav></Nav> */}
      <Link href="/register" color="blue.400" _hover={{ color: "blue.500" }}>
        About
      </Link>
      <Box bg="tomato" w="100%" p={4} color="white">
        This is the Box
      </Box>
    </>
  );
}