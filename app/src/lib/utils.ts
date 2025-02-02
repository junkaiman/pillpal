import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export interface DetailsObj {
  description: string;
  interactions: object;
  sideEffects: object;
  imgUrl: string;
}
