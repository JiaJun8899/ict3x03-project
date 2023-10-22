"use client";

export const API_HOST = "http://localhost:8000/api";
export function updateForm(value, setter, theUse) {
  return setter((prev) => {
    console.log(theUse);
    return { ...prev, ...value };
  });
}
import { useToast } from "@chakra-ui/react";

export const Toaster = () => {
  const toast = useToast();
  // types are: "success", "info", "warning", "error"

  const makeToast = (newRes) => {
    toast({
      description: newRes.message,
      status: newRes.type,
      isClosable: true,
      duration: 5000,
      variant: "left-accent",
    });
  };

  return { makeToast };
};