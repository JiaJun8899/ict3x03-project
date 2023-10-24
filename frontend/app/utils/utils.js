"use client";

export const API_HOST = "http://localhost:8000/api";

export function updateForm(value, setter, theUse) {
  return setter((prev) => {
    console.log(theUse);
    return { ...prev, ...value };
  });
}