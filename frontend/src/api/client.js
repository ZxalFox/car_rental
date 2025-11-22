const API_BASE_URL = process.env.GATSBY_API_URL || "http://localhost:8000";

const getCookie = (name) => {
  if (typeof document === "undefined") {
    return null;
  }
  const cookie = document.cookie
    ?.split(";")
    .map((entry) => entry.trim())
    .find((entry) => entry.startsWith(`${name}=`));
  return cookie ? decodeURIComponent(cookie.split("=")[1]) : null;
};

const prepareBody = (body, headers) => {
  if (!body || body instanceof FormData || typeof body === "string") {
    return body;
  }
  if (!headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }
  return JSON.stringify(body);
};

export const apiFetch = async (endpoint, options = {}) => {
  const { method = "GET", body, headers = {}, ...rest } = options;
  const finalHeaders = { ...headers };
  const isSafeMethod = ["GET", "HEAD", "OPTIONS"].includes(
    method.toUpperCase()
  );
  const preparedBody = prepareBody(body, finalHeaders);

  if (!isSafeMethod) {
    const csrfToken = getCookie("csrftoken");
    if (csrfToken && !finalHeaders["X-CSRFToken"]) {
      finalHeaders["X-CSRFToken"] = csrfToken;
    }
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method,
    credentials: "include",
    headers: finalHeaders,
    body: preparedBody,
    ...rest,
  });

  const contentType = response.headers.get("content-type") || "";
  const isJson = contentType.includes("application/json");
  const data = isJson ? await response.json() : null;

  if (!response.ok) {
    const message =
      data?.detail ||
      data?.error ||
      data?.message ||
      response.statusText ||
      "Erro inesperado";
    const error = new Error(message);
    error.status = response.status;
    error.payload = data;
    throw error;
  }

  return data;
};

export const getSession = () => apiFetch("/api/session/");
export const loginSession = (username, password) =>
  apiFetch("/api/session/login/", {
    method: "POST",
    body: { username, password },
  });
export const logoutSession = () =>
  apiFetch("/api/session/logout/", {
    method: "POST",
  });

export const listActiveCars = () => apiFetch("/api/cars/");
export const listMyRentals = () => apiFetch("/api/rentals/my/");
export const createRental = (payload) =>
  apiFetch("/api/rentals/", {
    method: "POST",
    body: payload,
  });

  
