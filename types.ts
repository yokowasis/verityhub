import { SupabaseClient } from "@supabase/supabase-js";
import { Database } from "./supabase";

export type WInput = Window & {
  getVal(id: string): string;
  setVal(id: string, value: string): void;
  getAllVal(): Record<string, string>;
  slugify(text: string): string;
  replaceAll(str: string, find: string, replace: string): string;
  capitalize(str: string): string;
  digitGrouping(num: number): string;
  paddingZero(num: number, size?: number): string;
  imgURLtoBase64(url: string): Promise<string>;
  convertImgSrcToBase64(htmlString: string): Promise<string>;
  rp(
    url: string,
    method?: "GET" | "POST" | "PUT" | "DELETE" | "PATCH",
    body?: unknown,
    token?: string,
    contentType?: "application/json" | "application/x-www-form-urlencoded"
  ): Promise<unknown>;
  showModal(id: string): void;
  closeModal(id: string): void;
  randomLightColor(): string;
  randomDarkColor(): string;
  randomDigit(digitCount?: number): string;
  randomAlphaNumeric(length?: number): string;
  now(): Promise<{ now: string }>;
  newDate(
    datestring: string,
    timezone: "Asia/Jakarta" | "Asia/Makassar" | "Asia/Jayapura"
  ): Date;
  generatePDFFromDocx(
    templateURL: string,
    keyValues: { [placeholder: string]: string }
  ): void;
  toast: {
    push: (
      params:
        | {
            duration?: number;
            type?: "success" | "error" | "warning" | "info";
            title?: string;
            message: string;
          }
        | string
    ) => void;
    info: (content: string) => void;
    success: (content: string) => void;
    warn: (content: string) => void;
    error: (content: string) => void;
    loading: (content?: string) => void;
    hide: () => void;
  };
};

export type DBClient = SupabaseClient<Database>;
