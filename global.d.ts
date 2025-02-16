declare global {
  const student: {
    name: string;
    email: string;
  };
  const getVal: (key: string) => string;
  const toast: {
    success: (message: string) => void;
    error: (message: string) => void;
    loading: (message: string) => void;
    hide: (loadingRef?) => void;
  };
}

export {};
