import { computed, type Ref } from "vue";
import es from "./i18n/es";
import en from "./i18n/en";

export type Language = "es" | "en";

const translations = {
  es,
  en,
} as const;

export function useI18n(language: Ref<Language>) {
  return computed(() => translations[language.value]);
}