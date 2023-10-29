"use client";
import { DateTime } from "luxon";
export const API_HOST = "http://localhost:8000/api";

export function updateForm(value, setter, theUse) {
  return setter((prev) => {
    console.log(theUse);
    return { ...prev, ...value };
  });
}

export function convertTime(time) {
  const convertedTime = DateTime.fromISO(time)
    .toJSDate()
    .toLocaleString("en-SG");
  return convertedTime;
}