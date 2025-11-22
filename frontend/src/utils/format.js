const currencyFormatter = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

const dateFormatter = new Intl.DateTimeFormat("pt-BR", {
  timeZone: "UTC",
});

export const formatCurrency = (value) => {
  if (value === null || value === undefined || value === "") {
    return currencyFormatter.format(0);
  }
  const numeric = typeof value === "number" ? value : Number(value);
  return currencyFormatter.format(Number.isNaN(numeric) ? 0 : numeric);
};

export const formatDate = (value) => {
  if (!value) {
    return "";
  }
  try {
    return dateFormatter.format(new Date(value));
  } catch (err) {
    return String(value);
  }
};
