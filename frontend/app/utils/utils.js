"use client";
import { DateTime } from "luxon";
import axios from "axios";
export const API_HOST = "http://localhost:8000/api";

export function updateForm(value, setter, theUse) {
  return setter((prev) => {
    return { ...prev, ...value };
  });
}

export function convertTime(time) {
  const convertedTime = DateTime.fromISO(time)
    .toJSDate()
    .toLocaleString("en-SG");
  return convertedTime;
}

export async function getRole(setUserRole, setLoading) {
  try {
    const response = await axios.get(`${API_HOST}/check-auth`, {
      withCredentials: true,
    });
    setUserRole(response.data);
  } catch (error) {
    console.error("There was an fetching your role");
  } finally {
    setLoading(false);
  }
}
